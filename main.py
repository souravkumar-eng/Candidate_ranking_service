"""
FastAPI service for candidate ranking
"""

# ---------------------------------------------------
# Imports
# ---------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi.middleware.cors import CORSMiddleware

from recommender_model import RecommenderModel


# ---------------------------------------------------
# Load model ONCE at startup
# ---------------------------------------------------

model = RecommenderModel()


# ---------------------------------------------------
# FastAPI app
# ---------------------------------------------------

app = FastAPI(
    title="Candidate Ranking AI Service",
    description="Ranks candidates using AI + rule-based scoring",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Thread pool for ML inference
# ---------------------------------------------------

executor = ThreadPoolExecutor(max_workers=4)


# ---------------------------------------------------
# Request schemas
# ---------------------------------------------------

class Candidate(BaseModel):
    id: str
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = None
    projects: Optional[List[str]] = None  # accepted but ignored


class RankRequest(BaseModel):
    job_title: str
    job_description: str
    candidates: List[Candidate]


# ---------------------------------------------------
# Async helper
# ---------------------------------------------------

async def run_model_async(job_title: str, job_desc: str, candidates: list):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor,
        model.rank,
        job_title,
        job_desc,
        candidates
    )


# ---------------------------------------------------
# API endpoint
# ---------------------------------------------------

@app.post("/rank-candidates")
async def rank_candidates_api(payload: RankRequest):

    candidates_data = [c.dict() for c in payload.candidates]

    ranked_results = await run_model_async(
        payload.job_title,
        payload.job_description,
        candidates_data
    )

    return {
        "job_title": payload.job_title,
        "count": len(ranked_results),
        "results": ranked_results
    }