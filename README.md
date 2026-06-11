# AI Resume Analyzer

A modern AI-powered Resume Analyzer built with Flask and Google Gemini. The application allows users to upload PDF resumes, extracts the content, and generates intelligent resume insights through Gemini LLM.

**Live Demo:** https://resume-builder-navy-kappa-47.vercel.app/

**Demo Video:** `ResumeAnalyzer.mp4` (included in the repository)

---

## Overview

AI Resume Analyzer is designed to help job seekers evaluate and improve their resumes. The system extracts text from uploaded PDF resumes and uses Google's Gemini AI through LangChain to analyze resume quality and provide actionable feedback.

The application presents results in a clean and user-friendly interface instead of displaying raw JSON responses.

### Analysis Includes

* Overall Resume Score
* Technical Skills Found
* Improvement Suggestions
* Gap Checklist

---

## Live Demo

Try the deployed application:

https://resume-builder-navy-kappa-47.vercel.app/

For a complete walkthrough of the application and its features, watch the included demo video:

```text
ResumeAnalyzer.mp4
```

---

## Features

✅ Upload PDF resumes

✅ Extract resume content using PyPDF2

✅ Analyze resumes using Google Gemini AI

✅ Generate Overall Resume Score

✅ Identify Technical Skills

✅ Provide Improvement Suggestions

✅ Detect Missing Resume Sections through Gap Checklist

✅ Modern and Responsive User Interface


---

## Technology Stack

### Backend

* Python 3.10+
* Flask
* LangChain
* Google Gemini API
* LangChain Google Generative AI

### GEN AI 

* Google Gemini 2.5 Flash
* Prompt Engineering
* JSON Response Parsing

### Resume Processing

* PyPDF2
* Python Dotenv

### Frontend

* HTML5
* CSS3
* JavaScript

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/ResumeBuilder.git
cd ResumeBuilder
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
```

Get your API key from Google AI Studio.

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

Upload a PDF resume and wait for the AI analysis to complete.

---

## Project Workflow

```text
User Upload Resume
        │
        ▼
PDF Text Extraction
        │
        ▼
Google Gemini Analysis
        │
        ▼
Resume Evaluation
        │
        ▼
Results Dashboard
```

---

## Project Structure

```text
ResumeBuilder/
│
├── app.py
├── requirements.txt
├── .env
│
├── templates/
│   └── index.html
│
└── ResumeAnalyzer.mp4
```



---

## Future Enhancements

* DOCX Resume Support
* OCR Support for Scanned Resumes
* Resume PDF Report Export
* Job Description Matching
* ATS Compatibility Score
* Interview Question Generator
* Career Recommendation Engine
* User Authentication & History Tracking

---

## Developed By

### Tooba Rani

AI Engineer | Machine Learning Enthusiast | Python Developer

---
