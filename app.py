import json
import os
import re
import tempfile

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from PyPDF2 import PdfReader

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.config["ALLOWED_EXTENSIONS"] = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def resume_data_extractor(pdf_path):
    text_chunks = []

    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
    except Exception:
        return ""

    return "\n\n".join(text_chunks).strip()


def analyze_resume_with_gemini(resume_text):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing GOOGLE_API_KEY environment variable.")

    prompt_template = """
            
        You are an expert Resume Reviewer.

        Analyze the following resume and return ONLY valid JSON.

        Required Analysis:

        1. Overall Resume Score (0-100)
        2. Technical Skills Found
        3. Improvement Suggestions
        4. Gap Checklist

        Gap Checklist should evaluate whether the resume contains:
        - Education
        - Experience
        - Skills
        - Projects
        - Certifications

        Return JSON in the following format:

        {{
            "resume_score": 0,
            "technical_skills": [],
            "improvements": [],
            "gap_checklist": {{
                "education": true,
                "experience": true,
                "skills": true,
                "projects": false,
                "certifications": false
            }}
        }}

        Resume Text:
        {resume_text}
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    llm = GoogleGenerativeAI(api_key=api_key, model="gemini-2.5-flash", temperature=0.3)
    chain = prompt | llm
    raw_response = chain.invoke({"resume_text": resume_text})

    raw_text = None
    if isinstance(raw_response, dict):
        return raw_response
    if hasattr(raw_response, "content"):
        raw_text = raw_response.content
    elif hasattr(raw_response, "text"):
        raw_text = raw_response.text
    elif hasattr(raw_response, "output_text"):
        raw_text = raw_response.output_text
    elif hasattr(raw_response, "output"):
        raw_text = raw_response.output

    if isinstance(raw_text, list):
        raw_text = "".join([str(item) for item in raw_text])
    if isinstance(raw_text, dict):
        raw_text = json.dumps(raw_text)

    if raw_text is None:
        raw_text = str(raw_response)

    raw_text = str(raw_text).strip()
    
    # Clean markdown blocks if present
    cleaned_text = raw_text
    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text[7:]
    elif cleaned_text.startswith("```"):
        cleaned_text = cleaned_text[3:]
    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3]
    cleaned_text = cleaned_text.strip()
    
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        pass
        
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        pass
        
    # Robustly find the first JSON object using brace counting
    start = raw_text.find('{')
    if start != -1:
        brace_count = 0
        in_string = False
        escape_next = False
        for i in range(start, len(raw_text)):
            char = raw_text[i]
            if escape_next:
                escape_next = False
                continue
            if char == '\\':
                escape_next = True
            elif char == '"':
                in_string = not in_string
            elif not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        extracted = raw_text[start:i+1]
                        try:
                            return json.loads(extracted)
                        except json.JSONDecodeError:
                            pass
                        break

    raise ValueError("Unable to parse Gemini response as JSON.\n" + raw_text)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No resume file provided."}), 400

    resume_file = request.files["resume"]
    if resume_file.filename == "":
        return jsonify({"error": "No resume file selected."}), 400

    if not allowed_file(resume_file.filename):
        return jsonify({"error": "Only PDF files allowed."}), 400

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        resume_file.save(temp_file.name)
        temp_path = temp_file.name

    try:
        resume_text = resume_data_extractor(temp_path)
        if not resume_text:
            return jsonify({"error": "No text found in resume."}), 400

        analysis = analyze_resume_with_gemini(resume_text)
        return jsonify({"status": "success", "analysis": analysis})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 502
    except Exception as exc:
        return jsonify({"error": "Gemini API unavailable or failed.", "details": str(exc)}), 500
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


if __name__ == "__main__":
    app.run(debug=True)
