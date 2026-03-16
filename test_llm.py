from llm_explainer import generate_batch_pros_cons

test = generate_batch_pros_cons(
    "Python ML Engineer",
    "Looking for Python and ML",
    [
        {
            "candidate_id": "C1",
            "skills": ["Python", "ML"],
            "projects": ["ML Project"],
            "experience_years": 2,
            "final_score": 80
        }
    ]
)

print(test)