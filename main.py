"""
main.py

FastAPI service that exposes the AI-based candidate ranking model.

Responsibilities:
- Load a pickled recommender model ONCE at startup
- Accept job + candidate data from external software
- Run ML inference asynchronously (non-blocking)
- Return ranked candidates with scores

This file is the ENTRY POINT of the service.
"""

# ---------------------------------------------------
# Imports
# ---------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import pickle
import asyncio
from concurrent.futures import ThreadPoolExecutor


# ---------------------------------------------------
# Load model at startup (VERY IMPORTANT)
# ---------------------------------------------------
# The model is loaded ONCE when the server starts.
# This avoids reloading heavy ML models per request.

with open("model/recommender.pkl", "rb") as f:
    model = pickle.load(f)


# ---------------------------------------------------
# FastAPI application instance
# ---------------------------------------------------

app = FastAPI(
    title="Candidate Ranking AI Service",
    description="Ranks candidates using hybrid AI + rule-based scoring",
    version="1.0.0"
)


# ---------------------------------------------------
# Thread pool for ML inference
# ---------------------------------------------------
# SentenceTransformer inference is CPU-bound.
# Running it directly in async event loop would block the server.
# ThreadPoolExecutor allows multiple requests to be processed safely.

executor = ThreadPoolExecutor(max_workers=4)


# ---------------------------------------------------
# Request data schemas (Input validation)
# ---------------------------------------------------

class Candidate(BaseModel):
    """
    Candidate data structure.

    Fields are optional to support incomplete data
    from external systems.
    """
    id: str
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = None
    projects: Optional[List[str]] = None


class RankRequest(BaseModel):
    """
    Request payload structure expected by the API.
    """
    job_title: str
    job_description: str
    candidates: List[Candidate]


# ---------------------------------------------------
# Async helper function to run ML safely
# ---------------------------------------------------
# This function runs the blocking ML model
# inside a thread pool so FastAPI remains responsive.

async def run_model_async(job_title: str, job_desc: str, candidates: list):
    """
    Runs the model ranking in a background thread.

    This prevents blocking the FastAPI event loop.
    """
    loop = asyncio.get_event_loop()

    return await loop.run_in_executor(
        executor,          # Thread pool
        model.rank,        # Model method
        job_title,         # Arguments passed to model.rank()
        job_desc,
        candidates
    )


# ---------------------------------------------------
# API Endpoint
# ---------------------------------------------------

@app.post("/rank-candidates")
async def rank_candidates_api(payload: RankRequest):
    """
    POST /rank-candidates

    This endpoint:
    - Receives job and candidate data from other software
    - Runs the recommender model
    - Returns ranked candidates with scores
    """

    # Convert Pydantic objects to plain dictionaries
    candidates_data = [c.dict() for c in payload.candidates]

    # Run the model asynchronously
    ranked_results = await run_model_async(
        payload.job_title,
        payload.job_description,
        candidates_data
    )

    # Return response to calling software
    return {
        "job_title": payload.job_title,
        "total_candidates": len(payload.candidates),
        "ranked_candidates": ranked_results
    }






# {
#   "job_title": ""Python Machine Learning Engineer"",
#   "job_description": "We are hiring a Python Machine Learning Engineer with at least 2 years of experience. Strong knowledge of Python, Machine Learning, SQL, and hands-on experience building ML models, scoring engines, APIs, or recommendation systems is required.",
#   "candidates": [
#   {"id":"C1","skills":["Python","Machine Learning","SQL"],"experience_years":2,"projects":["ML Scoring Engine","Recommendation System"]},
#   {"id":"C2","skills":["Python","Data Analysis","Pandas"],"experience_years":1,"projects":["Sales Dashboard"]},
#   {"id":"C3","skills":["Java","Spring Boot"],"experience_years":3,"projects":["Payment API"]},
#   {"id":"C4","skills":["Python","FastAPI","SQL"],"experience_years":2,"projects":["Backend API","Auth Service"]},
#   {"id":"C5","skills":["Python","Machine Learning"],"experience_years":4,"projects":["Fraud Detection","Risk Model"]},
#   {"id":"C6","skills":["SQL","Tableau"],"experience_years":3,"projects":["BI Dashboard"]},
#   {"id":"C7","skills":["Python"],"experience_years":1},
#   {"id":"C8","skills":["Python","ML","NLP"],"experience_years":2,"projects":["Resume Parser","Chatbot"]},
#   {"id":"C9","skills":["JavaScript","React"],"experience_years":2,"projects":["Frontend Dashboard"]},
#   {"id":"C10","skills":["Python","SQL","ML"],"experience_years":3,"projects":["Candidate Ranking Engine"]},

#   {"id":"C11","skills":["Python","FastAPI"],"experience_years":2,"projects":["Microservice API"]},
#   {"id":"C12","skills":["Python","Statistics"],"experience_years":1,"projects":["Hypothesis Testing"]},
#   {"id":"C13","skills":["Java","Hibernate"],"experience_years":4},
#   {"id":"C14","skills":["Python","Machine Learning","TensorFlow"],"experience_years":3,"projects":["Image Classifier"]},
#   {"id":"C15","skills":["SQL","Power BI"],"experience_years":2},
#   {"id":"C16","skills":["Python","Flask"],"experience_years":1,"projects":["REST API"]},
#   {"id":"C17","skills":["Python","ML","SQL"],"experience_years":2,"projects":["ML Pipeline","ETL System"]},
#   {"id":"C18","skills":["C++","DSA"],"experience_years":3},
#   {"id":"C19","skills":["Python","FastAPI","ML"],"experience_years":4,"projects":["Scoring Engine"]},
#   {"id":"C20","skills":["Python","Data Science"],"experience_years":2},

#   {"id":"C21","skills":["Python","ML"],"experience_years":5,"projects":["AI Hiring Tool"]},
#   {"id":"C22","skills":["Python","SQL"],"experience_years":1},
#   {"id":"C23","skills":["Python","Machine Learning"],"experience_years":2,"projects":["Spam Classifier"]},
#   {"id":"C24","skills":["Python","FastAPI","Docker"],"experience_years":3},
#   {"id":"C25","skills":["Data Analysis","Excel"],"experience_years":2},
#   {"id":"C26","skills":["Python","ML","NLP"],"experience_years":1},
#   {"id":"C27","skills":["Python","SQL","ETL"],"experience_years":4,"projects":["Data Pipeline"]},
#   {"id":"C28","skills":["Java","Spring"],"experience_years":2},
#   {"id":"C29","skills":["Python","ML"],"experience_years":3,"projects":["Risk Prediction"]},
#   {"id":"C30","skills":["Python","Statistics","SQL"],"experience_years":2},

#   {"id":"C31","skills":["Python","Machine Learning"],"experience_years":2},
#   {"id":"C32","skills":["Python","Flask","SQL"],"experience_years":3},
#   {"id":"C33","skills":["Python"],"experience_years":1},
#   {"id":"C34","skills":["Python","ML","Deep Learning"],"experience_years":5,"projects":["Vision Model"]},
#   {"id":"C35","skills":["SQL","Reporting"],"experience_years":2},
#   {"id":"C36","skills":["Python","FastAPI","ML"],"experience_years":2},
#   {"id":"C37","skills":["Python","ML"],"experience_years":3,"projects":["Recommendation Engine"]},
#   {"id":"C38","skills":["JavaScript","Node.js"],"experience_years":2},
#   {"id":"C39","skills":["Python","Data Analysis"],"experience_years":1},
#   {"id":"C40","skills":["Python","ML","SQL"],"experience_years":4},

#   {"id":"C41","skills":["Python","FastAPI"],"experience_years":2},
#   {"id":"C42","skills":["Python","Machine Learning"],"experience_years":3},
#   {"id":"C43","skills":["Python","SQL"],"experience_years":1},
#   {"id":"C44","skills":["Python","ML","AI"],"experience_years":5,"projects":["AI Matching System"]},
#   {"id":"C45","skills":["SQL","Tableau"],"experience_years":3},
#   {"id":"C46","skills":["Python","FastAPI","ML"],"experience_years":2},
#   {"id":"C47","skills":["Python","ML"],"experience_years":1},
#   {"id":"C48","skills":["Python","Machine Learning","SQL"],"experience_years":2,"projects":["Scoring Engine"]},
#   {"id":"C49","skills":["Java"],"experience_years":4},
#   {"id":"C50","skills":["Python","ML","SQL"],"experience_years":3}
# ]

   
# }