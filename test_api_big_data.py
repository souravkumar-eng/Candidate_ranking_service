import json
import requests
import time

URL = "http://127.0.0.1:8000/rank-candidates"

with open("big_test_payload.json") as f:
    payload = json.load(f)

start = time.time()
response = requests.post(URL, json=payload)
end = time.time()

print("Status:", response.status_code)
print("Time taken:", round(end - start, 2), "seconds")

data = response.json()

print("Job title:", data.get("job_title"))
print("Total candidates processed:", data.get("count"))

print("\nTop 5 results:")
for r in data["results"][:5]:
    print(r)
