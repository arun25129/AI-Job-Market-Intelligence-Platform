import pandas as pd
from recommend import recommend_jobs

data = {
    "Job Title": [
        "Data Analyst",
        "Machine Learning Engineer",
        "Psychiatrist",
        "Editor film/video",
        "Python Developer",
        "Neurosurgeon"
    ],
    "Skills": [
        "Python, SQL, Power BI",
        "Python, Machine Learning, TensorFlow",
        "Healthcare, Psychology",
        "Video Editing, Media",
        "Python, Django, SQL",
        "Medical, Surgery"
    ]
}

df = pd.DataFrame(data)

user_skills = ["Python", "SQL", "Machine Learning"]

recommended = recommend_jobs(
    df,
    user_skills,
    top_n=10
)

print("\nRecommended Jobs:")
print(recommended)