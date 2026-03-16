# ----------------------------
# Imports
# ----------------------------

import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from filter_engine import FilterEngine
from scoring_engine import ScoringEngine
from boost_engine import BoostEngine


class RecommenderModel:
    """
    Candidate ranking model.

    Responsibilities:
    - Load embedding model once
    - Apply strict filters
    - Compute semantic + rule-based scores
    - Apply boosts (optional)
    - Return full ranked structure
    """

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.encoder = SentenceTransformer(model_name)

    # ----------------------------
    # Helper Functions
    # ----------------------------

    def _embed(self, text: str):
        return self.encoder.encode(text, normalize_embeddings=True)

    def _safe_list(self, value):
        return value if isinstance(value, list) else []

    def _safe_int(self, value):
        return value if isinstance(value, int) else None

    def _candidate_to_text(self, candidate: dict):
        skills = self._safe_list(candidate.get("skills"))
        projects = self._safe_list(candidate.get("projects"))
        experience = self._safe_int(candidate.get("experience_years"))

        parts = []

        if skills:
            parts.append(f"Skills: {', '.join(skills)}")

        if projects:
            parts.append(f"Projects: {', '.join(projects)}")

        if experience is not None:
            parts.append(f"Experience: {experience} years")

        return ". ".join(parts)

    # ----------------------------
    # Experience Scoring
    # ----------------------------

    def _experience_score(self, job_desc: str, exp):

        if exp is None:
            return 0.3

        match = re.search(r"(\d+)\s+years", job_desc.lower())

        if not match:
            return 0.7

        required = int(match.group(1))

        if required == 0:
            return 0.7

        return min(exp / required, 1.0)

    # ----------------------------
    # Main Ranking Function
    # ----------------------------

    def rank(
        self,
        job_title,
        job_description,
        candidates,
        filters=None,
        scoring_weights=None
    ):

        # ---------------------------------
        # 1️Apply Strict Filters
        # ---------------------------------

        filtered_candidates = FilterEngine.apply_filters(
            candidates,
            filters or {}
        )

        if not filtered_candidates:
            return {
                "total_candidates": len(candidates),
                "filtered_candidates": 0,
                "ranked_results": []
            }

        # ---------------------------------
        # 2️Default Weights If Not Provided
        # ---------------------------------

        if not scoring_weights:
            scoring_weights = {
                "semantic": 0.30,
                "skills": 0.30,
                "experience": 0.20,
                "projects": 0.20
            }

        ScoringEngine.validate_weights(scoring_weights)

        # ---------------------------------
        # 3️Embed Job Description Once
        # ---------------------------------

        job_desc_emb = self._embed(job_description)

        # ---------------------------------
        # 4️Batch Embed Candidates
        # ---------------------------------

        candidate_texts = [
            self._candidate_to_text(c)
            for c in filtered_candidates
        ]

        candidate_embeddings = self.encoder.encode(
            candidate_texts,
            normalize_embeddings=True
        )

        results = []

        # ---------------------------------
        # 5️Score Each Candidate
        # ---------------------------------

        for idx, candidate in enumerate(filtered_candidates):

            candidate_id = candidate.get("id", "UNKNOWN")
            skills = self._safe_list(candidate.get("skills"))
            projects = self._safe_list(candidate.get("projects"))

            if not skills:
                continue

            cand_emb = candidate_embeddings[idx]

            # Semantic similarity
            desc_similarity = float(
                cosine_similarity([job_desc_emb], [cand_emb])[0][0]
            )

            # Skill semantic match
            skill_score = 0.0

            if skills:
                skill_embeddings = self.encoder.encode(
                    skills,
                    normalize_embeddings=True
                )

                matched = 0

                for skill_emb in skill_embeddings:
                    sim = cosine_similarity(
                        [job_desc_emb],
                        [skill_emb]
                    )[0][0]

                    if sim >= 0.65:
                        matched += 1

                skill_score = matched / len(skills)

            experience_score = self._experience_score(
                job_description,
                candidate.get("experience_years")
            )

            project_score = 1.0 if projects else 0.5

            # ---------------------------------
            # 6️ Dynamic Weighted Score
            # ---------------------------------

            final_score = ScoringEngine.compute_score(
                scoring_weights,
                desc_similarity,
                skill_score,
                experience_score,
                project_score
            )

            # ---------------------------------
            # 7️Optional Boost (Safe)
            # ---------------------------------

            if filters:
                final_score = BoostEngine.apply_boosts(
                    candidate,
                    filters,
                    final_score
                )

            results.append({
                "candidate_id": candidate_id,
                "final_score": round(final_score * 100, 2),
                "candidate_data": candidate
            })

        # ---------------------------------
        # 8️Sort Ranking
        # ---------------------------------

        ranked = sorted(
            results,
            key=lambda x: x["final_score"],
            reverse=True
        )

        return {
            "total_candidates": len(candidates),
            "filtered_candidates": len(filtered_candidates),
            "ranked_results": ranked
        }