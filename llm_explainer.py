import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

# --------------------------------------------------
# Load Environment Variables (.env support)
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not set in environment variables")

client = OpenAI(api_key=api_key)

MODEL_NAME = "gpt-4o"


# --------------------------------------------------
# Utility: Safe List
# --------------------------------------------------

def safe_list(value):
    return value if isinstance(value, list) else []


# --------------------------------------------------
# Utility: Clean & Extract JSON
# --------------------------------------------------

def extract_json(text):
    if not text:
        return None

    text = text.strip()

    # Remove markdown fences if model returns ```json
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print("Invalid JSON from OpenAI")
        return None


# --------------------------------------------------
# Main Function
# --------------------------------------------------

# def generate_batch_pros_cons(job_title, job_desc, top_candidates):

#     if not top_candidates:
#         return []

#     # -----------------------------------------
#     # Build Structured Candidate Input
#     # -----------------------------------------

#     candidates_payload = []

#     for c in top_candidates:
#         candidates_payload.append({
#             "candidate_id": c.get("candidate_id"),
#             "skills": safe_list(c.get("skills")),
#             "projects": safe_list(c.get("projects")),
#             "experience_years": c.get("experience_years"),
#             "final_score": c.get("final_score")
#         })

#     # -----------------------------------------
#     # Strict Prompt
#     # -----------------------------------------

#     prompt = f"""
# You are a professional hiring assistant.

# Job Title:
# {job_title}

# Job Description:
# {job_desc}

# For EACH candidate:

# 1. Generate EXACTLY 3 strengths (pros)
# 2. Generate EXACTLY 3 weaknesses (cons)
# 3. Use ONLY the provided data
# 4. Do NOT invent anything

# Return ONLY valid JSON array.

# Format:

# [
#   {{
#     "candidate_id": "C1",
#     "pros": ["...", "...", "..."],
#     "cons": ["...", "...", "..."]
#   }}
# ]

# Candidates:
# {json.dumps(candidates_payload)}
# """

#     # -----------------------------------------
#     # Call OpenAI
#     # -----------------------------------------

#     try:
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[
#                 {"role": "system", "content": "Return only valid JSON."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.2
#         )

#         raw_output = response.choices[0].message.content
#         print("RAW LLM OUTPUT:\n", raw_output)

#     except Exception as e:
#         print("OpenAI API error:", e)
#         return []

#     # -----------------------------------------
#     # Parse JSON
#     # -----------------------------------------

#     parsed = extract_json(raw_output)

#     if not parsed:
#         return []

#     if isinstance(parsed, list):
#         return parsed

#     if isinstance(parsed, dict):
#         if "candidates" in parsed:
#             return parsed["candidates"]
#         if "candidate_id" in parsed:
#             return [parsed]

#     return []


BATCH_SIZE = 5

def generate_batch_pros_cons(job_title, job_desc, top_candidates):

    if not top_candidates:
        return []

    all_results = []

    for i in range(0, len(top_candidates), BATCH_SIZE):

        batch = top_candidates[i:i+BATCH_SIZE]

        candidates_payload = []

        for c in batch:
            candidates_payload.append({
                "candidate_id": c.get("candidate_id"),
                "skills": safe_list(c.get("skills"))[:5],
                "projects": safe_list(c.get("projects"))[:2],
                "experience_years": c.get("experience_years"),
                "final_score": round(c.get("final_score",0),2)
            })

        prompt = f"""
You are a professional hiring assistant.

Job Title:
{job_title}

Job Description:
{job_desc}

For EACH candidate:

1. Generate EXACTLY 3 strengths (pros)
2. Generate EXACTLY 3 weaknesses (cons)
3. Use ONLY the provided data
4. Do NOT invent anything

Return ONLY valid JSON array.

Candidates:
{json.dumps(candidates_payload)}
"""

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            raw_output = response.choices[0].message.content
            parsed = extract_json(raw_output)

            if isinstance(parsed, list):
                all_results.extend(parsed)

        except Exception as e:
            print("LLM batch error:", e)

    return all_results