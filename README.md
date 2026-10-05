# AI Resume Intelligence & Career Assistant

A modern, production-quality AI-powered resume analyzer, job matcher, and career assistant built with Python, Streamlit, and modern NLP/AI tools.

## ✨ Features
- **Smart Resume Parsing**: Extracts name, contact info, skills, experience, and education from PDFs.
- **Explainable ATS Scoring**: Calculates an ATS score with a clear breakdown based on matching skills, experience, and formatting.
- **Semantic Job Matching**: Compares your resume to a target job description using semantic similarity (Sentence-Transformers).
- **Skill Gap Analysis**: Identifies missing critical skills for your target role.
- **AI Resume Assistant**: Chat with your resume, get project improvement suggestions, generate a professional summary, and create custom interview questions.
- **Learning Roadmap**: Generates a week-by-week learning plan for missing skills.
- **Admin Dashboard**: Analytics and reporting on all parsed resumes.

## 🏗️ Architecture

```
AI-Resume-Analyzer/
├── app.py                # Main Streamlit application entry point
├── pages/                # Streamlit pages (Dashboard, Analyzer, Chat, Admin, Feedback)
├── modules/              # Core business logic
│   ├── resume_parser.py  # PDF text extraction and NLP-based entity recognition
│   ├── ats_scorer.py     # Weighted ATS scoring engine
│   ├── jd_matcher.py     # Semantic matching with sentence-transformers
│   └── resume_improver.py# LLM-based generative AI tasks (Gemini)
├── database/             # Database connection and schema setup
├── utils/                # Helper utilities
├── tests/                # Unit tests
├── .env                  # Environment variables for DB & API Keys
└── requirements.txt      # Project dependencies
```

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.8+
- MySQL Database

### 2. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Environment Variables
Copy `.env.example` to `.env` and configure your credentials:
```bash
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=cv

# For generative AI features (Chat, Interview Prep, Resume Tips)
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Run the Application
```bash
streamlit run app.py
```
