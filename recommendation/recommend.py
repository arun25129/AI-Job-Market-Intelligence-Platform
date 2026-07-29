import pandas as pd


def recommend_jobs(df, user_skills, top_n=5):
    if df.empty:
        return df

    user_skills = [
        skill.strip().lower()
        for skill in user_skills
        if skill.strip()
    ]

    relevant_keywords = [
        "python",
        "data analyst",
        "data scientist",
        "data engineer",
        "machine learning",
        "ml engineer",
        "ai engineer",
        "python developer",
        "python programmer",
        "software developer",
        "software engineer",
        "sql developer",
        "business analyst"
    ]

    def calculate_match(row):
        job_skills = str(row.get("Skills", "")).lower()
        job_title = str(row.get("Job Title", "")).lower()

        skill_score = 0
        title_score = 0

        for skill in user_skills:
            if skill in job_skills:
                skill_score += 1

            if skill in job_title:
                title_score += 3

        title_is_relevant = any(
            keyword in job_title
            for keyword in relevant_keywords
        )

        if not title_is_relevant:
            return 0

        return skill_score + title_score

    result = df.copy()

    result["Match Score"] = result.apply(
        calculate_match,
        axis=1
    )

    result = result[result["Match Score"] > 0]
    result = result.sort_values(
        by="Match Score",
        ascending=False
    )

    result = result.head(top_n).copy()

    if not result.empty:
        max_score = result["Match Score"].max()
        result["Match %"] = (
            (result["Match Score"] / max_score) * 100
        ).round().astype(int).astype(str) + "%"

    return result