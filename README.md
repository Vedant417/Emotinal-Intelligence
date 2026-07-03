# 🎭 EmotionIQ – AI-Powered Movie Performance Prediction Platform

EmotionIQ is a full-stack AI-powered analytics platform that predicts how audiences are likely to emotionally respond to a movie before its release or after launch. By analyzing story elements, themes, emotional intensity, audience appeal, and cinematic attributes, the platform generates an overall performance score along with actionable recommendations to improve audience engagement.

Designed for production studios, distributors, streaming platforms, and content creators, EmotionIQ combines AI reasoning with intelligent scoring algorithms to help evaluate a movie's commercial and emotional potential.

Built using FastAPI, React, Python, and Large Language Models (LLMs), the platform delivers production-ready emotional intelligence through an interactive dashboard.

---

# 📂 Project Structure

```
EmotionIQ/
│
├── backend/
│   ├── venv/
│   ├── main.py
│   ├── models.json
│   ├── test.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── DiagnosisResult.jsx
│   │   │   ├── MovieForm.jsx
│   │   │   └── SymptomForm.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# ✨ Features

### 🎬 AI Movie Performance Prediction

Predict the potential audience response and commercial performance of a movie using AI-driven emotional analysis.

---

### 📊 Overall Performance Score

Generate a comprehensive performance score based on multiple emotional and storytelling factors.

---

### ❤️ Emotional Intelligence Analysis

Evaluate key emotional dimensions including:

- Audience Engagement
- Emotional Impact
- Storytelling Strength
- Character Appeal
- Entertainment Value
- Viewer Satisfaction

---

### 📈 Performance Insights

Identify strengths and weaknesses that influence audience reception and predict overall success.

---

### 💡 AI Improvement Recommendations

Receive intelligent recommendations for improving emotional impact, audience connection, pacing, storytelling, and commercial appeal.

---

### 🎯 Content Optimization

Analyze opportunities to enhance:

- Story Structure
- Character Development
- Emotional Depth
- Audience Retention
- Market Appeal

---

### 📄 Interactive Dashboard

Modern React dashboard providing:

- Overall Score
- Emotional Breakdown
- Performance Indicators
- AI Suggestions
- Visual Analytics

---

### ⚡ Fast AI Processing

FastAPI-powered backend delivers quick AI inference with efficient request handling.

---

### 🔌 REST API Architecture

Modular backend exposing scalable REST APIs for movie analysis, scoring, recommendations, and reporting.

---

# 🛠️ Technologies Used

## Frontend

- React.js
- Vite
- JavaScript
- CSS3

---

## Backend

- FastAPI
- Python
- REST APIs

---

## Artificial Intelligence

- Google Gemini
- Large Language Models (LLMs)
- Prompt Engineering
- Emotional Intelligence Analysis
- AI Scoring Engine

---

## Data Processing

- JSON
- Python
- Pydantic

---

## Tools

- Git
- GitHub
- VS Code
- Postman

---

# 💻 System Requirements

Minimum Requirements

- Python 3.10+
- Node.js 18+
- npm
- Internet connection for AI services

Recommended

- Python 3.11
- Node.js 20+

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/EmotionIQ.git

cd EmotionIQ
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file inside the backend folder.

Example:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Run Backend

```bash
uvicorn main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# 🧠 How It Works

1. User enters movie details and analysis parameters.

2. The backend processes movie information and contextual metadata.

3. AI models evaluate emotional storytelling, audience engagement, and cinematic quality.

4. The scoring engine generates an overall performance score.

5. AI provides detailed reasoning and improvement suggestions.

6. Results are displayed through an interactive React dashboard.

---

# 📊 Analysis Workflow

```
Movie Information
        │
        ▼
Data Processing
        │
        ▼
AI Emotional Analysis
        │
        ▼
Performance Scoring
        │
        ▼
Recommendation Engine
        │
        ▼
Interactive Dashboard
```

---

# 🔧 Troubleshooting

### Gemini API Errors

Verify the API key is correctly configured inside the `.env` file.

---

### Backend Connection Issues

Ensure the FastAPI server is running before starting the frontend.

---

### Frontend Cannot Reach Backend

Verify API URLs and CORS configuration.

---

### Dependency Errors

Install all required packages using:

```bash
pip install -r requirements.txt
```

---

# 🚀 Future Enhancements

- Audience Demographic Prediction
- Regional Performance Analysis
- Box Office Revenue Prediction
- Streaming Success Forecasting
- Genre Comparison Dashboard
- Multi-Movie Benchmarking
- Cloud Deployment
- Docker Support
- Export Analysis Reports
- Team Collaboration

---

# 📝 License

This project is developed for educational, research, and enterprise AI demonstration purposes.

---

## 👨‍💻 Developer

**Vedant Vyas**

AI Engineer | Full Stack Developer

Built as an enterprise AI platform for predicting movie performance using emotional intelligence and Large Language Models.
