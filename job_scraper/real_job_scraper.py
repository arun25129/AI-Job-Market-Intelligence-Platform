import requests
from bs4 import BeautifulSoup

url = "https://realpython.github.io/fake-jobs/"

response = requests.get(url)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

jobs = soup.find_all("div", class_="card-content")

print("Total Jobs Found:", len(jobs))

for job in jobs:

    title = job.find("h2").text.strip()

    company = job.find("h3").text.strip()

    location = job.find("p", class_="location").text.strip()
    apply_link = job.find("a")["href"]

    print("Job Title :", title)
    print("Company   :", company)
    print("Location  :", location)
    print("Apply Link:", apply_link)
    print("-" * 50)