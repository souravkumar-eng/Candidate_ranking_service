

# ----------------------------
# Imports
# ----------------------------

import re  # Used to extract required experience from job description text
from sentence_transformers import SentenceTransformer  # Converts text → embeddings
from sklearn.metrics.pairwise import cosine_similarity  # Measures similarity between embeddings


class RecommenderModel:
    """
    Main recommendation model class.

    Responsibilities:
    - Load embedding model once
    - Convert job & candidate text to vectors
    - Compute relevance scores
    - Return ranked candidate list
    """

    def __init__(
        self,
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        job_desc_weight=0.60,
        job_title_weight=0.15,
        skill_weight=0.15,
        experience_weight=0.10
    ):
        # """
        # Initialize model and scoring weights.

        # All weights must sum to 1.0 to keep scoring normalized.
        # """

        # Validate weight configuration
        total = (
            job_desc_weight +
            job_title_weight +
            skill_weight +
            experience_weight
        )
        assert abs(total - 1.0) < 0.01, "Weights must sum to 1.0"

        # Store weights
        self.job_desc_weight = job_desc_weight
        self.job_title_weight = job_title_weight
        self.skill_weight = skill_weight
        self.experience_weight = experience_weight

        # Load sentence transformer model once (important for performance)
        self.encoder = SentenceTransformer(model_name)

    # ----------------------------
    # Helper Functions
    # ----------------------------

    def _embed(self, text: str):
        """
        Convert text into a normalized embedding vector.
        Normalization ensures cosine similarity behaves correctly.
        """
        return self.encoder.encode(text, normalize_embeddings=True)

    def _safe_list(self, value):
        """
        Ensure value is a list.
        Returns empty list if value is missing or invalid.
        """
        return value if isinstance(value, list) else []

    def _safe_int(self, value):
        """
        Ensure value is an integer.
        Returns None if experience is missing.
        """
        return value if isinstance(value, int) else None

    def _candidate_to_text(self, candidate: dict):
        """
        Convert candidate structured data into a single text string.

        This text is used for semantic embedding.
        """

        skills = self._safe_list(candidate.get("skills"))  # mandatory
        projects = self._safe_list(candidate.get("projects"))
        experience = self._safe_int(candidate.get("experience_years"))

        # Skills always included
        parts = [f"Skills: {', '.join(skills)}"]

        # Projects add credibility
        if projects:
            parts.append(f"Projects: {', '.join(projects)}")

        # Experience adds seniority signal
        if experience is not None:
            parts.append(f"Experience: {experience} years")

        return ". ".join(parts)

    # ----------------------------
    # Rule-Based Scoring Functions
    # ----------------------------

    def _skill_score(self, job_desc: str, skills):
        """
        Skill relevance score:
        Measures overlap between job description words and candidate skills.
        """

        job_words = set(job_desc.lower().split())
        skill_words = set(s.lower() for s in skills)

        # Percentage of skills mentioned in job description
        return len(job_words & skill_words) / len(skill_words)

    def _experience_score(self, job_desc: str, exp):
        """
        Experience score:
        - Missing experience → penalty
        - If job specifies years, score is proportional
        """

        # Missing experience → penalize
        if exp is None:
            return 0.3

        # Extract required years from job description
        match = re.search(r"(\d+)\s+years", job_desc.lower())
        if not match:
            return 0.7  # Experience exists but requirement not specified

        required = int(match.group(1))
        if required == 0:
            return 0.7

        return min(exp / required, 1.0)

    # ----------------------------
    # Main Ranking Function
    # ----------------------------

    def rank(self, job_title: str, job_description: str, candidates: list):
        """
        Rank candidates for a given job.

        Inputs:
        - job_title: role intent
        - job_description: detailed responsibilities
        - candidates: list of candidate dictionaries

        Output:
        - List of candidates sorted by final_score (descending)
        """

        # Embed job title and description once
        job_title_emb = self._embed(job_title)
        job_desc_emb = self._embed(job_description)

        results = []

        # Evaluate each candidate
        for candidate in candidates:
            candidate_id = candidate.get("id", "UNKNOWN")

            # ----------------------------
            # Mandatory Skills Check
            # ----------------------------

            skills = candidate.get("skills")
            if not skills:
                # Skip invalid candidates (industry-standard behavior)
                continue

            projects = self._safe_list(candidate.get("projects"))

            # Build candidate semantic profile
            candidate_text = self._candidate_to_text(candidate)
            cand_emb = self._embed(candidate_text)

            # ----------------------------
            # Semantic Similarity Scores
            # ----------------------------

            # Role intent similarity
            title_similarity = float(
                cosine_similarity([job_title_emb], [cand_emb])[0][0]
            )

            # Responsibility/context similarity
            desc_similarity = float(
                cosine_similarity([job_desc_emb], [cand_emb])[0][0]
            )

            # ----------------------------
            # Rule-Based Scores
            # ----------------------------

            skill_score = self._skill_score(job_description, skills)

            experience_score = self._experience_score(
                job_description, candidate.get("experience_years")
            )

            # ----------------------------
            # Missing Project Penalty
            # ----------------------------

            # Candidates without projects are slightly penalized
            project_penalty = 0.85 if not projects else 1.0

            # ----------------------------
            # Final Score Calculation
            # ----------------------------

            final_score = (
                self.job_desc_weight * desc_similarity +
                self.job_title_weight * title_similarity +
                self.skill_weight * skill_score +
                self.experience_weight * experience_score
            ) * project_penalty

            # Store final result
            results.append({
                "candidate_id": candidate_id,
                "job_desc_score": round(desc_similarity * 100, 2),
                "job_title_score": round(title_similarity * 100, 2),
                "skill_score": round(skill_score * 100, 2),
                "experience_score": round(experience_score * 100, 2),
                "final_score": round(float(final_score) * 100, 2)
            })

        # Return ranked candidates (best first)
        return sorted(results, key=lambda x: x["final_score"], reverse=True)
