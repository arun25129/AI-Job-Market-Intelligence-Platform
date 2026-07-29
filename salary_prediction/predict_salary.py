import joblib
import os
import pandas as pd


model_path = os.path.join(
    os.path.dirname(__file__),
    "salary_model.pkl"
)


model = joblib.load(model_path)

def predict_salary(experience, skills_count, job_role):

    input_data = pd.DataFrame(
        [[experience, skills_count, job_role]],
        columns=["experience", "skills_count", "job_role"]
    )

    predicted_salary = model.predict(input_data)[0]

    return round(predicted_salary, 2)


if __name__ == "__main__":
    experience = 3
    skills_count = 5
    job_role = 2

    salary = predict_salary(
        experience,
        skills_count,
        job_role
    )

    print("Experience:", experience, "years")
    print("Number of Skills:", skills_count)
    print("Job Role:", job_role)
    print("Predicted Salary: ₹", salary)