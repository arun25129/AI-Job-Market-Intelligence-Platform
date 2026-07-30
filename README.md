# AI Job Market Intelligence Platform

An AI-powered job market analysis platform built with **Python, PostgreSQL, Machine Learning, NLP, and Streamlit**.

The platform analyzes job-market data, provides interactive analytics, recommends jobs based on user skills, extracts skills from resumes, and predicts salary packages.

## Key Features

- Interactive Job Market Dashboard
- Job Search and Filtering
- Company-wise and Location-wise Analysis
- Experience and Skill Analysis
- Job Recommendation System
- Skill-Based Job Matching
- Match Score and Match Percentage
- PDF Resume Upload
- Resume Skill Extraction
- Salary Prediction
- Annual and Monthly Salary Estimation
- Salary Package Prediction in LPA
- Career Growth Insights

## Tech Stack

**Programming**
- Python

**Database**
- PostgreSQL
- SQL

**Machine Learning & Data**
- Machine Learning
- NLP
- Pandas

**Dashboard & Visualization**
- Streamlit
- Plotly

**Development Tools**
- Git
- GitHub
- VS Code
- pgAdmin

## Project Structure

    AI-Job-Market-Intelligence-Platform/
    |
    |-- backend/
    |-- dashboard/
    |-- database/
    |-- job_scraper/
    |-- recommendation/
    |-- resume_parser/
    |-- salary_prediction/
    |
    |-- requirements.txt
    |-- .gitignore
    |-- LICENSE
    |-- README.md

## Job Recommendation System

Users can enter their skills manually or upload a PDF resume.

The system compares the user's skills with job requirements and returns the best matching jobs with:

- Company
- Location
- Required Skills
- Match Score
- Match Percentage

## Resume Parser

The resume parser extracts text from uploaded PDF resumes and identifies relevant technical skills.

These extracted skills can then be used by the recommendation system to find suitable jobs.

## Salary Prediction

The salary prediction module estimates salary using information such as:

- Job Role
- Experience
- Number of Skills

The system provides:

- Predicted Annual Salary
- Estimated Package (LPA)
- Estimated Monthly Salary
- Salary Level
- Career Growth Indicator

## Dashboard

The Streamlit dashboard provides an interactive interface for exploring job-market information.

Users can filter jobs based on:

- Location
- Company
- Experience
- Skills
- Salary Range
- Posted Date

## Installation

Clone the repository:

    git clone https://github.com/arun25129/AI-Job-Market-Intelligence-Platform.git

Move into the project directory:

    cd AI-Job-Market-Intelligence-Platform

Install dependencies:

    pip install -r requirements.txt

## Run the Application

Start the Streamlit application:

    streamlit run dashboard/app.py

Then open the local Streamlit address shown in the terminal.

## Future Improvements

- Live job API integration
- Advanced NLP-based resume analysis
- Improved ML salary prediction model
- Cloud deployment
- User authentication
- Personalized career recommendations

## Author

**Arun Kumar**

B.Tech Computer Science & Engineering  
Data Science & Analysis  
DIT University, Dehradun

GitHub: @arun25129

## License

This project is licensed under the MIT License.
