import requests
from bs4 import BeautifulSoup
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ai_job_market",
    user="postgres",
    password="root",
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


    title = job.find("h2").text.strip()

    company = job.find("h3").text.strip()

    location = job.find("p", class_="location").text.strip()

    cursor.execute("""
INSERT INTO jobs
(job_title, company, location)
VALUES (%s, %s, %s)
""", (
    title,
    company,
    location
))
 

    print("Title:", title)
    print("Company:", company)
    print("Location:", location)
    print("-" * 50)

    conn.commit()

print("✅ All jobs saved successfully!")

cursor.close()
conn.close()