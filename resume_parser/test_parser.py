from parser import extract_skills

resume_text = """
I am a Data Science student.
I have experience with Python, SQL, Machine Learning,
Pandas, NumPy, Git and Streamlit.
"""

skills = extract_skills(resume_text)

print("Extracted Skills:")
print(skills)