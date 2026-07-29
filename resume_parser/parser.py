import re
from pypdf import PdfReader


SKILLS = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "data analysis",
    "data science",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "power bi",
    "tableau",
    "excel",
    "postgresql",
    "mysql",
    "git",
    "github",
    "nlp",
    "streamlit"
]


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found_skills.append(skill.title())

    return found_skills
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text