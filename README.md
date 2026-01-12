# Candidate Ranking AI Service

A production-ready **AI-powered candidate ranking microservice** built using **FastAPI** and **Sentence Transformers**.  
The service ranks 50–100 candidates against a job role using a **hybrid intelligence approach** (AI + rule-based logic).

This system is designed to integrate seamlessly with **ATS platforms, HR software, and internal hiring tools**.

---

## ARCHITECTURE>>

┌──────────────────────────────┐
│        External Software      │
│  (ATS / HR / Hiring Platform) │
└───────────────┬──────────────┘
                │
                │ POST /rank-candidates
                │ (job + candidates JSON)
                ▼
┌──────────────────────────────┐
│        FastAPI Service        │
│   (Async REST Microservice)  │
│                              │
│  - Input validation (Pydantic)
│  - Async request handling     │
└───────────────┬──────────────┘
                │
                │ ThreadPoolExecutor
                │ (CPU-bound inference)
                ▼
┌──────────────────────────────┐
│   RecommenderModel (Pickled)  │
│                              │
│  - Semantic similarity (AI)   │
│  - Skill rule scoring         │
│  - Experience rule scoring    │
│  - Project penalty logic      │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│     Ranked Candidates JSON   │
│  (sorted by final_score)     │
└──────────────────────────────┘


## 🧠 Key Features

- ✅ Hybrid scoring (AI semantic similarity + business rules)
- ✅ Handles incomplete / noisy candidate data gracefully
- ✅ FastAPI-based async microservice
- ✅ Pickled ML model loaded once at startup
- ✅ Scales to 100+ candidates per request
- ✅ Ready for cloud deployment (Render)

---

## 🏗️ Architecture Overview

External Software (ATS / HR Tool)
|
| POST /rank-candidates (JSON)
|
FastAPI Service
|
| Async Execution
|
RecommenderModel (Pickled)
|
| AI + Rules
|
Ranked Candidate Scores (JSON)

yaml
Copy code

---

## 🧮 Scoring Strategy (Hybrid Intelligence)

Final candidate score is computed using:

Final Score =
(job_description_similarity * 0.60)

(job_title_similarity * 0.15)

(skill_match_score * 0.15)

(experience_match_score * 0.10)

yaml
Copy code

### Why Hybrid?
- **AI** understands meaning and context
- **Rules** enforce business constraints
- This mirrors how **real ATS systems work**

---

## 📁 Project Structure

candidate_ranking_service/
│
├── main.py # FastAPI application (API layer)
├── recommender_model.py # Core AI + rule-based model
├── save_model.py # Script to generate .pkl model
├── test_model.py # Model testing script
├── requirements.txt # Python dependencies
│
├── model/
│ └── recommender.pkl # Serialized trained model
│
└── README.md

yaml
Copy code

---

## ⚙️ Tech Stack

- **Python 3.10+**
- **FastAPI**
- **Sentence Transformers**
- **Scikit-learn**
- **PyTorch**
- **Uvicorn**

---

## 🚀 Getting Started (Local Setup)

### 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd candidate_ranking_service
2️⃣ Create Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
💾 Create Pickled Model
Run once to generate the model file:

bash
Copy code
python save_model.py
This creates:

bash
Copy code
model/recommender.pkl
🧪 Test Model (Without API)
bash
Copy code
python test_model.py
Ensures:

Model loads correctly

Ranking works

Missing fields do not crash the system

🌐 Run FastAPI Service
bash
Copy code
uvicorn main:app --reload
Open browser:

arduino
Copy code
http://127.0.0.1:8000/docs
Swagger UI allows interactive API testing.

🔗 API Endpoint
POST /rank-candidates
Request Body (Example)
json
Copy code
{
  "job_title": "Python Machine Learning Engineer",
  "job_description": "Python ML engineer with 2+ years experience",
  "candidates": [
    {
      "id": "C1",
      "skills": ["Python", "Machine Learning", "SQL"],
      "experience_years": 2,
      "projects": ["ML Scoring Engine"]
    },
    {
      "id": "C2",
      "skills": ["Python"],
      "experience_years": 1
    }
  ]
}
Response (Example)
json
Copy code
{
  "job_title": "Python Machine Learning Engineer",
  "total_candidates": 2,
  "ranked_candidates": [
    {
      "candidate_id": "C1",
      "final_score": 84.23
    },
    {
      "candidate_id": "C2",
      "final_score": 42.11
    }
  ]
}





