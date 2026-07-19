import requests
from bs4 import BeautifulSoup

url = "https://realpython.github.io/fake-jobs/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "lxml")

jobs = soup.find_all("div", class_="card-content")

for job in jobs:

    title = job.find("h2", class_="title").text.strip()

    company = job.find("h3", class_="company").text.strip()

    location = job.find("p", class_="location").text.strip()

    apply_link = job.find("a")["href"]

    print("Job Title :", title)
    print("Company   :", company)
    print("Location  :", location)
    print("Apply Link:", apply_link)
    print("-" * 60)