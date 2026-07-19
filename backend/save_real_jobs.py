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

