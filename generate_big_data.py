import json
import random

SKILLS_POOL = [
    "Python", "SQL", "FastAPI", "Flask", "Django",
    "Machine Learning", "Data Structures", "Algorithms",
    "System Design", "REST APIs", "Docker", "Microservices"
]

PROJECTS_POOL = [
    "Backend API",
    "Microservice System",
    "Recommendation Engine",
    "ETL Pipeline",
    "Analytics Dashboard",
    "ML Pipeline",
    "Authentication Service"
]

def generate_candidate(idx):
    candidate = {
        "id": f"C{idx}",
        "skills": random.sample(SKILLS_POOL, random.randint(2, 5))
    }

    # 60% have experience
    if random.random() < 0.6:
        candidate["experience_years"] = random.randint(0, 8)

    # 50% have projects
    if random.random() < 0.5:
        candidate["projects"] = random.sample(PROJECTS_POOL, random.randint(1, 3))

    return candidate


def generate_payload(n=5000):
    return {
        "job_title": "Software Engineer",
        "job_description": (
            "We are hiring a Software Engineer with strong Python, SQL, and API development "
            "experience. The candidate should have experience building scalable backend systems, "
            "REST APIs, and working with databases. Knowledge of system design and microservices is a plus."
        ),
        "candidates": [generate_candidate(i) for i in range(1, n + 1)]
    }


if __name__ == "__main__":
    payload = generate_payload(50000)

    with open("big_test_payload.json", "w") as f:
        json.dump(payload, f, indent=2)

    print("Generated big_test_payload.json with 1000000 candidates")
