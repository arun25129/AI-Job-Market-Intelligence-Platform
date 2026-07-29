import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os



data = {
    "experience": [0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
    "skills_count": [2, 3, 4, 4, 5, 6, 6, 7, 8, 10],
    "job_role": [1, 1, 2, 2, 2, 3, 3, 3, 4, 4],
    "salary": [
        300000,
        400000,
        500000,
        600000,
        700000,
        850000,
        950000,
        1100000,
        1250000,
        1500000
    ]
}

df = pd.DataFrame(data)

X = df[["experience", "skills_count", "job_role"]]


y = df["salary"]


model = LinearRegression()
model.fit(X, y)


model_path = os.path.join(
    os.path.dirname(__file__),
    "salary_model.pkl"
)

joblib.dump(model, model_path)

print("Salary prediction model trained successfully!")
print("Model saved at:", model_path)