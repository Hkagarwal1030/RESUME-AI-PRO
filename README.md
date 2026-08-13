# RESUME-AI-PRO

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/license/mit/)

A modern Flask-based AI resume analyzer that helps users understand their current profile, discover missing skills, and receive a tailored roadmap for their next career move.

## ✨ Features
- Resume text input or PDF/DOCX upload
- AI-powered skill gap analysis
- Personalized roadmap suggestions
- Interview question generation
- Premium landing page and dashboard experience

## 📸 Preview
## 📸 Project Screenshots

| Sign Up | Login |
|---------|-------|
| <img src="Screenshot/singup.png" width="450"> | <img src="Screenshot/login.png" width="450"> |

| Dashboard |
|-----------|
| <img src="Screenshot/dashboard.png" width="900"> |

| Analysis Results |
|------------------|
| <img src="Screenshot/analysis-results.png" width="900"> |

| Learning Roadmap |
|------------------|
| <img src="Screenshot/roadmap.png" width="900"> |

| Interview Preparation |
|------------------------|
| <img src="Screenshot/interview-prep.png" width="900"> |

## 🖼️ Project Brand
![RESUME-AI-PRO Logo](docs/logo.svg)

## 🚀 Getting Started
1. Create and activate a virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a local environment file from [.env.example](.env.example)
4. Run the app:
   ```bash
   python app.py
   ```
5. Open: http://127.0.0.1:5000

## 🌐 Deploy to the Public Internet
This app is now ready for a public deployment. The safest free setup is Render with a hosted database.

### Recommended deployment flow
1. Push the project to GitHub.
2. Create a Render account and import the repository.
3. Add these environment variables in Render:
   - `SECRET_KEY`
   - `OPENROUTER_API_KEY`
   - `OPENROUTER_MODEL`
   - `DATABASE_URL`
4. Use the included [render.yaml](render.yaml) and [Procfile](Procfile) files.
5. Deploy the service and share the generated public URL.

### Environment values
- `SECRET_KEY`: any long random string
- `OPENROUTER_API_KEY`: your OpenRouter API key
- `OPENROUTER_MODEL`: usually `openai/gpt-oss-20b:free`
- `DATABASE_URL`: MySQL/Postgres connection string from your cloud database

> For a public app, do not rely on your local machine or local SQLite database. Use a hosted database so everyone can access the same app and data.

## 🧠 Tech Stack
- Flask
- SQLAlchemy
- Jinja2
- HTML/CSS/JavaScript

## 📁 Project Structure
- app.py — Flask routes and app setup
- templates/ — HTML pages
- static/ — CSS and assets
- models.py / db.py — database models and connection

## 📝 Notes
- The app is designed for resume-based career guidance and skill planning.
- Replace the AI logic in ai.py with your preferred model or API integration.

