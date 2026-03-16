class ScoringEngine:

    @staticmethod
    def validate_weights(weights):

        if isinstance(weights, dict):
            semantic = weights.get("semantic", 0)
            skills = weights.get("skills", 0)
            experience = weights.get("experience", 0)
            projects = weights.get("projects", 0)
        else:
            semantic = weights.semantic
            skills = weights.skills
            experience = weights.experience
            projects = weights.projects

        total = semantic + skills + experience + projects

        if abs(total - 1.0) > 0.01:
            raise ValueError("Weights must sum to 1.0")

    @staticmethod
    def compute_score(
        weights,
        semantic_score,
        skill_score,
        experience_score,
        project_score
    ):

        if isinstance(weights, dict):
            return (
                weights.get("semantic", 0) * semantic_score +
                weights.get("skills", 0) * skill_score +
                weights.get("experience", 0) * experience_score +
                weights.get("projects", 0) * project_score
            )

        return (
            weights.semantic * semantic_score +
            weights.skills * skill_score +
            weights.experience * experience_score +
            weights.projects * project_score
        )
    