# """
# FastAPI service for candidate ranking
# """

# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List, Optional
# import asyncio
# from concurrent.futures import ThreadPoolExecutor
# from fastapi.middleware.cors import CORSMiddleware

# from recommender_model import RecommenderModel
# from llm_explainer import generate_batch_pros_cons


# # ----------------------------
# # Load Model Once
# # ----------------------------

# model = RecommenderModel()

# app = FastAPI(
#     title="Candidate Ranking AI Service",
#     description="Ranks candidates using AI + rule-based scoring",
#     version="2.0.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# executor = ThreadPoolExecutor(max_workers=4)


# # ----------------------------
# # Schemas
# # ----------------------------

# class Candidate(BaseModel):
#     id: str
#     skills: Optional[List[str]] = None
#     experience_years: Optional[int] = None
#     projects: Optional[List[str]] = None

#     location: Optional[str] = None
#     gender: Optional[str] = None
#     expected_salary: Optional[float] = None
#     notice_period_days: Optional[int] = None
#     education_level: Optional[str] = None
#     industry_experience: Optional[List[str]] = None


# class Filters(BaseModel):
#     location: Optional[str] = None
#     gender_preference: Optional[str] = None
#     max_salary_budget: Optional[float] = None
#     max_notice_period: Optional[int] = None
#     education_required: Optional[str] = None
#     industry_required: Optional[str] = None


# class ScoringWeights(BaseModel):
#     semantic: float = 0.30
#     skills: float = 0.30
#     experience: float = 0.20
#     projects: float = 0.20


# class RankRequest(BaseModel):
#     job_title: str
#     job_description: str
#     filters: Optional[Filters] = None
#     scoring_weights: Optional[ScoringWeights] = None
#     candidates: List[Candidate]


# # ----------------------------
# # Async Wrapper
# # ----------------------------

# async def run_model_async(
#     job_title: str,
#     job_desc: str,
#     candidates: list,
#     filters=None,
#     scoring_weights=None
# ):
#     loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(
#         executor,
#         model.rank,
#         job_title,
#         job_desc,
#         candidates,
#         filters,
#         scoring_weights
#     )


# # ----------------------------
# # API Endpoint
# # ----------------------------

# @app.post("/rank-candidates")
# async def rank_candidates_api(payload: RankRequest):

#     # Convert Pydantic models → dict
#     candidates_data = [c.model_dump() for c in payload.candidates]
#     filters_data = payload.filters.model_dump() if payload.filters else {}
#     scoring_weights_data = (
#         payload.scoring_weights.model_dump()
#         if payload.scoring_weights else {}
#     )

#     # ----------------------------
#     # 1️Run Ranking Engine
#     # ----------------------------

#     rank_output = await run_model_async(
#         payload.job_title,
#         payload.job_description,
#         candidates_data,
#         filters_data,
#         scoring_weights_data
#     )

#     ranked_results = rank_output["ranked_results"]
#     total_candidates = rank_output["total_candidates"]
#     filtered_candidates = rank_output["filtered_candidates"]

#     # Handle empty results
#     if not ranked_results:
#         return {
#             "job_title": payload.job_title,
#             "total_candidates": total_candidates,
#             "filtered_candidates": 0,
#             "count": 0,
#             "results": []
#         }

#     # ----------------------------
#     # 2️Prepare Top 20 for LLM
#     # ----------------------------

#     top_20 = ranked_results[:20]

#     llm_input = [
#         {
#             "candidate_id": item["candidate_id"],
#             **item["candidate_data"],
#             "final_score": item["final_score"]
#         }
#         for item in top_20
#     ]

#     # ----------------------------
#     # 3️Call LLM Once
#     # ----------------------------

#     explanations = generate_batch_pros_cons(
#         payload.job_title,
#         payload.job_description[:800],
#         llm_input
#     )

#     # ----------------------------
#     # 4️Merge LLM Output
#     # ----------------------------

#     explanation_map = {}

#     if isinstance(explanations, list):
#         explanation_map = {
#             str(e.get("candidate_id")).strip(): e
#             for e in explanations
#             if e.get("candidate_id")
#         }

#     final_results = []

#     for item in ranked_results:
#         cid = str(item["candidate_id"]).strip()
#         explanation = explanation_map.get(cid, {})

#         final_results.append({
#             "candidate_id": cid,
#             "final_score": item["final_score"],
#             "pros": explanation.get("pros", []),
#             "cons": explanation.get("cons", [])
#         })

#     # ----------------------------
#     # 5️Final Response
#     # ----------------------------

#     return {
#         "job_title": payload.job_title,
#         "total_candidates": total_candidates,
#         "filtered_candidates": filtered_candidates,
#         "count": len(ranked_results),
#         "results": final_results
#     }

"""
FastAPI service for candidate ranking
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi.middleware.cors import CORSMiddleware

from recommender_model import RecommenderModel
from llm_explainer import generate_batch_pros_cons


# ----------------------------
# Load Model Once
# ----------------------------

model = RecommenderModel()

app = FastAPI(
    title="Candidate Ranking AI Service",
    description="Ranks candidates using AI + rule-based scoring",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ThreadPoolExecutor(max_workers=4)


# ----------------------------
# Schemas
# ----------------------------

class Candidate(BaseModel):
    id: str
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = None
    projects: Optional[List[str]] = None

    location: Optional[str] = None
    gender: Optional[str] = None
    expected_salary: Optional[float] = None
    notice_period_days: Optional[int] = None
    education_level: Optional[str] = None
    industry_experience: Optional[List[str]] = None


class Filters(BaseModel):
    location: Optional[str] = None
    gender_preference: Optional[str] = None
    max_salary_budget: Optional[float] = None
    max_notice_period: Optional[int] = None
    education_required: Optional[str] = None
    industry_required: Optional[str] = None


class ScoringWeights(BaseModel):
    semantic: float = 0.30
    skills: float = 0.30
    experience: float = 0.20
    projects: float = 0.20


class RankRequest(BaseModel):
    job_title: str
    job_description: str
    filters: Optional[Filters] = None
    scoring_weights: Optional[ScoringWeights] = None
    candidates: List[Candidate]


# ----------------------------
# Async Wrapper
# ----------------------------

async def run_model_async(
    job_title: str,
    job_desc: str,
    candidates: list,
    filters=None,
    scoring_weights=None
):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor,
        model.rank,
        job_title,
        job_desc,
        candidates,
        filters,
        scoring_weights
    )


# ----------------------------
# API Endpoint
# ----------------------------

@app.post("/rank-candidates")
async def rank_candidates_api(payload: RankRequest):

    # Convert Pydantic → dict
    candidates_data = [c.model_dump() for c in payload.candidates]
    filters_data = payload.filters.model_dump() if payload.filters else {}
    scoring_weights_data = (
        payload.scoring_weights.model_dump()
        if payload.scoring_weights else {}
    )

    # ----------------------------
    # 1️Run Ranking Engine
    # ----------------------------

    rank_output = await run_model_async(
        payload.job_title,
        payload.job_description,
        candidates_data,
        filters_data,
        scoring_weights_data
    )

    ranked_results = rank_output["ranked_results"]
    total_candidates = rank_output["total_candidates"]
    filtered_candidates = rank_output["filtered_candidates"]

    if not ranked_results:
        return {
            "job_title": payload.job_title,
            "total_candidates": total_candidates,
            "filtered_candidates": 0,
            "count": 0,
            "results": []
        }

    # ----------------------------
    # 2️ Prepare Top 20 For LLM
    # ----------------------------

    top_20 = ranked_results[:20]

    llm_input = [
        {
            "candidate_id": item["candidate_id"],
            **item["candidate_data"],
            "final_score": item["final_score"]
        }
        for item in top_20
    ]

    # ----------------------------
    # 3️Call LLM Safely
    # ----------------------------

    explanation_map = {}

    try:
        explanations_raw = generate_batch_pros_cons(
            payload.job_title,
            payload.job_description,
            llm_input
        )

        print("RAW LLM OUTPUT:", explanations_raw)

        # Normalize possible formats
        if isinstance(explanations_raw, dict) and "candidates" in explanations_raw:
            parsed_list = explanations_raw["candidates"]

        elif isinstance(explanations_raw, list):
            parsed_list = explanations_raw

        else:
            parsed_list = []

        for item in parsed_list:
            cid = str(item.get("candidate_id")).strip()
            if cid:
                explanation_map[cid] = {
                    "pros": item.get("pros", []),
                    "cons": item.get("cons", [])
                }

    except Exception as e:
        print("LLM ERROR:", str(e))
        explanation_map = {}

    # ----------------------------
    # 4️Merge Ranking + LLM (Fail-Safe)
    # ----------------------------

    final_results = []

    for item in ranked_results:

        cid = str(item["candidate_id"]).strip()
        explanation = explanation_map.get(cid)

        # Fallback if LLM fails
        if not explanation:
            explanation = {
                "pros": ["Profile matches ranking criteria"],
                "cons": ["Detailed AI explanation unavailable"]
            }

        final_results.append({
            "candidate_id": cid,
            "final_score": item["final_score"],
            "pros": explanation.get("pros", []),
            "cons": explanation.get("cons", [])
        })

    # ----------------------------
    # 5️Final Response
    # ----------------------------

    return {
        "job_title": payload.job_title,
        "total_candidates": total_candidates,
        "filtered_candidates": filtered_candidates,
        "count": len(ranked_results),
        "results": final_results
    }