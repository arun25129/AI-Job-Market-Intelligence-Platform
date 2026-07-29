import requests
from bs4 import BeautifulSoup
import psycopg2
import streamlit as st

conn = psycopg2.connect(
    host="aws-0-ap-northeast-1.pooler.supabase.com",
    database="postgres",
    user="postgres.bxjgyyyjwmwpuixbkwhl",
    password=st.secrets["SUPABASE_PASSWORD"],
    port="5432"
)

cursor = conn.cursor()

print("✅ Database Connected!")

url = "https://realpython.github.io/fake-jobs/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

jobs = soup.find_all("div", class_="card-content")

print("Total Jobs Found:", len(jobs))

for job in jobs:
    title = job.find("h2", class_="title").text.strip()
    company = job.find("h3", class_="company").text.strip()
    location = job.find("p", class_="location").text.strip()

    salary = "Not Mentioned"
    experience = "Not Mentioned"
    skills = "Python"
    job_description = "Scraped from Real Python Fake Jobs"
    posted_date = "2026-07-19"
    source = "RealPython"
    job_url = url

    cursor.execute("""
        INSERT INTO jobs
        (job_title, company, location, salary, experience, skills,
        job_description, posted_date, source, job_url)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            title,
            company,
            location,
            salary,
            experience,
            skills,
            job_description,
            posted_date,
            source,
            job_url
        ))

    print(title)
    print(company)
    print(location)
    print("-" * 50)

conn.commit()

print("✅ All jobs saved successfully!")