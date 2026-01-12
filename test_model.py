from recommender_model import RecommenderModel

model = RecommenderModel()

job_title = "Python Machine Learning Engineer"

job_description = (
    "We are hiring a Python Developer with at least 2 years of experience. "
    "The candidate must have strong knowledge of Machine Learning and SQL. "
    "Hands-on experience in building ML systems, scoring engines, "
    "recommendation systems, or data pipelines is highly preferred. "
    "Experience with APIs, model deployment, and analytics tools is a plus."
)
candidates = [
    {"id":"C1","skills":["Python","Machine Learning","SQL"],"experience_years":3,
     "projects":["Resume Parser","Recommendation Engine"]},

    {"id":"C2","skills":["Python","SQL"],"experience_years":2,
     "projects":["ETL Pipeline","Data Warehouse"]},

    {"id":"C3","skills":["Java","Spring","Hibernate"],"experience_years":4,
     "projects":["ERP System","Billing App"]},

    {"id":"C4","skills":["Python","Machine Learning"],"experience_years":1,
     "projects":["Spam Classifier"]},

    {"id":"C5","skills":["Python","ML","SQL"],"experience_years":2,
     "projects":["AI Hiring Tool","Scoring Engine"]},

    {"id":"C6","skills":["Python","SQL"],"experience_years":5,
     "projects":["Analytics Dashboard"]},

    {"id":"C7","skills":["C++","DSA"],"experience_years":2,
     "projects":["Graph Visualizer"]},

    {"id":"C8","skills":["Python","Deep Learning","SQL"],"experience_years":3,
     "projects":["Image Classification","Face Recognition"]},

    {"id":"C9","skills":["Python","Flask"],"experience_years":1,
     "projects":["REST API"]},

    {"id":"C10","skills":["Python","Machine Learning","SQL"],"experience_years":3,
     "projects":["ML Pipeline","Recommendation Engine"]},

    # ---- Missing EXPERIENCE ----
    {"id":"C11","skills":["Python","SQL"],
     "projects":["CRUD App","Student Portal"]},

    {"id":"C12","skills":["Python","Machine Learning"],
     "projects":["Model Deployment","CI/CD for ML"]},

    {"id":"C13","skills":["Python","ML"]},

    {"id":"C14","skills":["JavaScript","React"],
     "projects":["Frontend Dashboard"]},

    {"id":"C15","skills":["Python"]},

    # ---- Missing PROJECTS ----
    {"id":"C16","skills":["Python","SQL"],"experience_years":1},

    {"id":"C17","skills":["Python","SQL","ML"],"experience_years":2},

    {"id":"C18","skills":["Java","Hibernate"],"experience_years":5},

    {"id":"C19","skills":["Python","Machine Learning"],"experience_years":2},

    {"id":"C20","skills":["Python","Machine Learning","SQL"],"experience_years":4},

    # ---- Mixed quality ----
    {"id":"C21","skills":["Python","ML"],"experience_years":2,
     "projects":["Sales Forecast"]},

    {"id":"C22","skills":["Python"],"experience_years":1},

    {"id":"C23","skills":["C#",".NET"],"experience_years":3,
     "projects":["Enterprise App"]},

    {"id":"C24","skills":["Python","Machine Learning","SQL"],"experience_years":5,
     "projects":["ML Registry","Model Monitoring"]},

    {"id":"C25","skills":["Python","Pandas","SQL"],"experience_years":2,
     "projects":["ETL Script"]},

    {"id":"C26","skills":["Python","Machine Learning"],
     "projects":["Clustering Tool"]},

    {"id":"C27","skills":["Java","Microservices"],"experience_years":6},

    {"id":"C28","skills":["Python","SQL","ML"],"experience_years":2,
     "projects":["ML REST API"]},

    {"id":"C29","skills":["Python","Flask","SQL"],"experience_years":2},

    {"id":"C30","skills":["Python","Machine Learning"],"experience_years":1},

    # ---- Mostly incomplete but valid ----
    {"id":"C31","skills":["Python"]},

    {"id":"C32","skills":["Python","SQL"],"experience_years":3},

    {"id":"C33","skills":["Python"],
     "projects":["Backend API"]},

    {"id":"C34","skills":["Python","ML","SQL"],"experience_years":2},

    {"id":"C35","skills":["Python","Statistics"],"experience_years":4},

    {"id":"C36","skills":["Python","NumPy"],"experience_years":1},

    {"id":"C37","skills":["Python","Machine Learning"],"experience_years":5,
     "projects":["End-to-End ML System"]},

    {"id":"C38","skills":["Java","SQL"],"experience_years":3},

    {"id":"C39","skills":["Python","SQL","Power BI"],"experience_years":2},

    {"id":"C40","skills":["Python","Deep Learning"],"experience_years":2},

    # ---- Edge but realistic ----
    {"id":"C41","skills":["Python","ML"],"projects":["Demand Planning"]},

    {"id":"C42","skills":["Python"],"experience_years":2},

    {"id":"C43","skills":["Python","Machine Learning","SQL"],"experience_years":6},

    {"id":"C44","skills":["Python","SQL"],"experience_years":4,
     "projects":["Reporting Tool"]},

    {"id":"C45","skills":["Python","Machine Learning"],
     "projects":["Fraud Detection"]},

    {"id":"C46","skills":["Python","Data Science"],"experience_years":3},

    {"id":"C47","skills":["Python","ML","SQL"],"experience_years":1},

    {"id":"C48","skills":["Python","MLOps"],"experience_years":4,
     "projects":["Model Deployment"]},

    {"id":"C49","skills":["Python","Flask","SQL"],"experience_years":1},

    {"id":"C50","skills":["Python","Machine Learning","SQL"],"experience_years":2,
     "projects":["Candidate Ranking System"]},

    # ---- Extra realistic noise ----
    {"id":"C51","skills":["Python","SQL"]},

    {"id":"C52","skills":["Python","Machine Learning"],"experience_years":3},

    {"id":"C53","skills":["Python","Data Analysis"],"experience_years":2},

    {"id":"C54","skills":["Python","ML"],"projects":["Prediction Tool"]},

    {"id":"C55","skills":["Python","SQL","Statistics"],"experience_years":4},

    {"id":"C56","skills":["Python"],"experience_years":1},

    {"id":"C57","skills":["Python","Machine Learning"],"experience_years":5},

    {"id":"C58","skills":["Python","SQL"],"projects":["Dashboard"]},

    {"id":"C59","skills":["Python","ML","SQL"],"experience_years":2},

    {"id":"C60","skills":["Python","Machine Learning","SQL"],"experience_years":3,
     "projects":["ML Optimization"]}
]






results = model.rank(
    job_title=job_title,
    job_description=job_description,
    candidates=candidates
)

for r in results:
    print(r)