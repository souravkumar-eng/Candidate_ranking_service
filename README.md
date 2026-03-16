# Candidate Ranking Service 🚀

AI-powered **candidate recommendation and ranking system** designed to evaluate and rank candidates against a job description using **semantic similarity, rule-based scoring, and LLM-based explanations**.

The system exposes a **FastAPI REST API** capable of evaluating thousands of candidates and returning ranked results with **pros and cons analysis**.

---

# 📌 Overview

Recruitment teams often receive hundreds or thousands of resumes. Manually screening them is slow and inconsistent.

This project solves that problem by:

1. Understanding **job requirements**
2. Evaluating **candidate skills, experience, and projects**
3. Computing **semantic similarity using embeddings**
4. Applying **rule-based scoring**
5. Generating **LLM-based explanations (Pros / Cons)**

The system outputs a **ranked list of candidates with explanations**.

---

# ⚙️ Key Features

✔ Candidate ranking using **semantic similarity**
✔ Rule-based **scoring engine**
✔ **LLM-generated pros & cons** for each candidate
✔ FastAPI-based **REST API**
✔ Handles **large batch candidate datasets**
✔ Dockerized for **production deployment**
✔ CI/CD deployment ready

---

# 🏗 System Architecture

```
Client Request
      │
      ▼
FastAPI API
      │
      ├── Filter Engine
      │
      ├── Scoring Engine
      │
      ├── Boost Engine
      │
      └── Recommender Model
            │
            ├── Sentence Embeddings
            ├── Semantic Similarity
            └── Ranking Logic
                    │
                    ▼
            LLM Explanation
            (Pros / Cons)
                    │
                    ▼
              Ranked Results
```

---

# 📂 Project Structure

```
Candidate_ranking_service
│
├── main.py                    # FastAPI application
├── recommender_model.py      # Candidate ranking model
├── scoring_engine.py         # Rule-based scoring
├── filter_engine.py          # Candidate filtering logic
├── boost_engine.py           # Score boosting logic
├── llm_explainer.py          # LLM-based pros/cons generator
│
├── generate_big_data.py      # Generate large candidate dataset
│
├── test_api.py               # API testing script
├── test_model.py             # Model testing
├── test_llm.py               # LLM explanation tests
│
├── big_test_payload.json     # Large test payload
│
├── Dockerfile                # Container configuration
├── requirements.txt          # Python dependencies
├── runtime.txt               # Python runtime
│
└── .env.example              # Environment variable template
```

---

# 🧠 How Candidate Ranking Works

### Step 1 — Job Understanding

The system reads:

```
job_title
job_description
```

---

### Step 2 — Candidate Parsing

Each candidate contains:

```
{
  "id": "C1",
  "skills": ["Python", "SQL"],
  "experience_years": 3,
  "projects": ["Backend API"]
}
```

---

### Step 3 — Semantic Similarity

Using **Sentence Transformers**, the system calculates:

```
Job Description Embedding
        vs
Candidate Profile Embedding
```

Similarity is computed using **cosine similarity**.

---

### Step 4 — Rule Based Scoring

Additional scoring factors:

* Required skills
* Experience years
* Relevant projects
* Skill overlap

---

### Step 5 — Score Boosting

Boosts candidates who match:

* critical skills
* system design experience
* backend development

---

### Step 6 — LLM Explanation

An LLM generates:

```
Pros
Cons
```

Example:

```
Pros
• Strong Python and API development skills
• Relevant backend project experience

Cons
• Limited system design experience
```

---

# Running the Project Locally

### 1️⃣ Clone the Repository

```
git clone https://github.com/souravkumar-eng/Candidate_ranking_service.git
cd Candidate_ranking_service
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv .venv
source .venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create `.env` file:

```
OPENAI_API_KEY=your_api_key
```

---

### 5️⃣ Start the API

```
uvicorn main:app --reload
```

Open API docs:

```
http://localhost:8000/docs
```

---

# 🐳 Running with Docker

Build container:

```
docker build -t candidate-ranking-api .
```

Run container:

```
docker run -d -p 8000:8000 --env-file .env candidate-ranking-api
```

Access API:

```
http://localhost:8000/docs
```

---

# 📊 Example API Request

POST `/rank-candidates`

```
{
  "job_title": "Software Engineer",
  "job_description": "Looking for Python backend developer with API experience",
  "candidates": [
    {
      "id": "C1",
      "skills": ["Python", "SQL", "FastAPI"],
      "experience_years": 3
    }
  ]
}
```

---

# 📊 Example Response

```
{
  "ranked_candidates": [
    {
      "id": "C1",
      "score": 0.87,
      "pros": ["Strong Python backend skills"],
      "cons": ["Limited system design exposure"]
    }
  ]
}
```

---

# 🧪 Load Testing

Generate large candidate dataset:

```
python generate_big_data.py
```

Test API with large payload:

```
python test_api_big_data.py
```

The system can evaluate **thousands of candidates per request**.

---

# ☁️ Deployment

The service can be deployed using:

* Docker
* AWS EC2
* GitHub Actions CI/CD

Production deployment flow:

```
Git Push
   ↓
GitHub Actions
   ↓
SSH to EC2
   ↓
Docker Build
   ↓
Container Restart
```

---

# 🛠 Tech Stack

| Technology            | Usage               |
| --------------------- | ------------------- |
| Python                | Backend             |
| FastAPI               | API framework       |
| Sentence Transformers | Semantic similarity |
| Scikit-learn          | Cosine similarity   |
| OpenAI                | LLM explanations    |
| Docker                | Containerization    |
| GitHub Actions        | CI/CD               |

---

# 📈 Future Improvements

Possible enhancements:

• Learning-to-Rank models
• Resume parsing
• Skill ontology matching
• Recruiter dashboard
• Candidate interview prediction

---

# 👨‍💻 Author

**Sourav Kumar**

AI / ML Engineer

GitHub
https://github.com/souravkumar-eng

---

# ⭐ If you found this project useful

Consider giving the repository a **star ⭐**

