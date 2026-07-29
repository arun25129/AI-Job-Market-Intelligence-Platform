import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recommendation.recommend import recommend_jobs
from resume_parser.parser import extract_text_from_pdf, extract_skills
from salary_prediction.predict_salary import predict_salary

st.set_page_config(
    page_title="AI Job Market Intelligence Platform",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI Job Market Intelligence Platform")
st.write("Welcome to the AI Job Market Intelligence Platform!")

conn = None
cursor = None


def load_jobs(_cursor):
    _cursor.execute("""
        SELECT 
            job_id, 
            job_title, 
            company, 
            location, 
            salary, 
            experience, 
            skills, 
            posted_date, 
            source
        FROM jobs
        ORDER BY job_id
    """)
    return _cursor.fetchall()


try:
    conn = psycopg2.connect(
        host="aws-0-ap-northeast-1.pooler.supabase.com",
        database="postgres",
        user="postgres.bxjgyyyjwmwpuixbkwhl",
        password=st.secrets["SUPABASE_PASSWORD"],
        port="5432"
    )
    cursor = conn.cursor()
    st.success("✅ Database Connected Successfully!")

    jobs = load_jobs(cursor)

    df_all = pd.DataFrame(
        jobs,
        columns=[
            "Job ID", "Job Title", "Company", "Location",
            "Salary", "Experience", "Skills", "Posted Date", "Source"
        ]
    )

    df = df_all.copy()

    st.sidebar.title("🎯 Filters")

    locations = ["All"] + sorted(df_all["Location"].dropna().unique().tolist())
    selected_location = st.sidebar.selectbox("📍 Select Location", locations)
    if selected_location != "All":
        df = df[df["Location"] == selected_location]

    companies = ["All"] + sorted(df_all["Company"].dropna().unique().tolist())
    selected_company = st.sidebar.selectbox("🏢 Select Company", companies)
    if selected_company != "All":
        df = df[df["Company"] == selected_company]

    experiences = ["All"] + sorted(df_all["Experience"].dropna().unique().tolist())
    selected_experience = st.sidebar.selectbox("👨‍💻 Select Experience", experiences)
    if selected_experience != "All":
        df = df[df["Experience"] == selected_experience]

    skills = ["All"] + sorted(df_all["Skills"].dropna().unique().tolist())
    selected_skill = st.sidebar.selectbox("🛠️ Select Skill", skills)
    if selected_skill != "All":
        df = df[df["Skills"].str.contains(selected_skill, case=False, na=False)]

    salary_filter = st.sidebar.selectbox(
        "💰 Salary Range",
        ["All", "Below 5 LPA", "5-10 LPA", "10-20 LPA", "Above 20 LPA"]
    )

    df["Posted Date"] = pd.to_datetime(df["Posted Date"], errors="coerce")

    min_date = df["Posted Date"].min()
    max_date = df["Posted Date"].max()

    if pd.notna(min_date) and pd.notna(max_date):
        selected_dates = st.sidebar.date_input(
            "📅 Posted Date Range",
            value=(min_date.date(), max_date.date()),
            min_value=min_date.date(),
            max_value=max_date.date()
        )

        if len(selected_dates) == 2:
            start_date, end_date = selected_dates
            df = df[
                (df["Posted Date"] >= pd.to_datetime(start_date)) &
                (df["Posted Date"] <= pd.to_datetime(end_date))
            ]

    if salary_filter != "All":
        numeric_salary = df["Salary"].astype(str).str.extract(r'(\d+\.?\d*)')[0]
        numeric_salary = pd.to_numeric(numeric_salary, errors="coerce")

        if salary_filter == "Below 5 LPA":
            df = df[numeric_salary < 5]
        elif salary_filter == "5-10 LPA":
            df = df[(numeric_salary >= 5) & (numeric_salary <= 10)]
        elif salary_filter == "10-20 LPA":
            df = df[(numeric_salary > 10) & (numeric_salary <= 20)]
        elif salary_filter == "Above 20 LPA":
            df = df[numeric_salary > 20]

    search = st.sidebar.text_input(
        "🔍 Search Jobs",
        placeholder="Enter Job Title, Company or Location..."
    )
    if search:
        df = df[
            df["Job Title"].str.contains(search, case=False, na=False) |
            df["Company"].str.contains(search, case=False, na=False) |
            df["Location"].str.contains(search, case=False, na=False)
        ]

    if st.sidebar.button("🔄 Reset Filters"):
        st.rerun()

    sort_option = st.sidebar.selectbox(
        "🔃 Sort Jobs",
        [
            "Latest Posted",
            "Highest Salary",
            "Company (A-Z)"
        ]
    )

    if sort_option == "Latest Posted":
        df["Posted Date"] = pd.to_datetime(df["Posted Date"], errors="coerce")
        df = df.sort_values(by="Posted Date", ascending=False)

    elif sort_option == "Highest Salary":
        df["Salary_Num"] = pd.to_numeric(
            df["Salary"].astype(str).str.extract(r'(\d+\.?\d*)')[0],
            errors="coerce"
        )
        df = df.sort_values(by="Salary_Num", ascending=False)

    elif sort_option == "Company (A-Z)":
        df = df.sort_values(by="Company")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "📈 Analytics",
        "📋 Job Listings",
        "🎯 Recommendations",
        "💰 Salary Prediction"
    ])

    with tab1:
        st.subheader("📊 Dashboard Overview")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💼 Total Jobs", len(df))
        with col2:
            st.metric("🏢 Companies", df["Company"].nunique())
        with col3:
            st.metric("📍 Locations", df["Location"].nunique())
        with col4:
            st.metric("🛠 Skills", df["Skills"].nunique())

        if not df.empty:
            top_company = df["Company"].value_counts().idxmax()
            top_company_jobs = df["Company"].value_counts().max()

            st.info(
                f"🏆 **Top Hiring Company:** {top_company} "
                f"({top_company_jobs} job postings)"
            )

        st.subheader("📊 Jobs by Source")
        if not df.empty and "Source" in df.columns:
            source_count = df["Source"].value_counts().reset_index()
            source_count.columns = ["Source", "Jobs"]

            fig_source = px.bar(
                source_count,
                x="Source",
                y="Jobs",
                text="Jobs",
                color="Jobs",
                title="Jobs by Source"
            )
            fig_source.update_traces(
                textposition="outside",
                hovertemplate="<b>%{x}</b><br>Jobs: %{y}<extra></extra>"
            )
            fig_source.update_layout(
                xaxis_title="Job Source",
                yaxis_title="Number of Jobs",
                height=450
            )
            st.plotly_chart(fig_source, use_container_width=True)
        else:
            st.info("No source data available for current filters.")

        st.subheader("🏢 Top 10 Companies Hiring")
        if not df.empty and "Company" in df.columns:
            company_count = (
                df["Company"]
                .value_counts()
                .head(10)
                .rename_axis("Company")
                .reset_index(name="Jobs")
            )

            fig_company = px.bar(
                company_count,
                x="Company",
                y="Jobs",
                color="Jobs",
                text="Jobs",
                title="Top 10 Companies Hiring"
            )
            fig_company.update_traces(textposition="outside")
            fig_company.update_layout(
                xaxis_title="Company",
                yaxis_title="Number of Jobs",
                xaxis_tickangle=-45,
                height=650,
                margin=dict(t=80, b=180)
            )
            st.plotly_chart(fig_company, use_container_width=True)
        else:
            st.info("No company data available.")

        st.subheader("🥧 Top 10 Job Locations")
        if not df.empty and "Location" in df.columns:
            location_count = (
                df["Location"]
                .value_counts()
                .head(10)
                .rename_axis("Location")
                .reset_index(name="Jobs")
            )

            fig_pie = px.pie(
                location_count,
                names="Location",
                values="Jobs",
                title="Top 10 Job Locations"
            )
            fig_pie.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No location data available for current filters.")

        st.subheader("👨‍💻 Jobs by Experience")
        if not df.empty and "Experience" in df.columns:
            experience_count = (
                df["Experience"]
                .fillna("Not Specified")
                .value_counts()
                .rename_axis("Experience")
                .reset_index(name="Jobs")
            )

            fig_experience = px.bar(
                experience_count,
                x="Experience",
                y="Jobs",
                color="Jobs",
                text="Jobs",
                title="Jobs by Experience"
            )
            fig_experience.update_traces(textposition="outside")
            fig_experience.update_layout(
                xaxis_title="Experience",
                yaxis_title="Number of Jobs",
                height=450
            )
            st.plotly_chart(fig_experience, use_container_width=True)
        else:
            st.info("No experience data available.")

    with tab2:
        st.subheader("💰 Salary Distribution")
        salary_df = df.copy()
        salary_df["Salary_Num"] = salary_df["Salary"].astype(str).str.extract(r'(\d+\.?\d*)')[0]
        salary_df["Salary_Num"] = pd.to_numeric(salary_df["Salary_Num"], errors="coerce")
        salary_df = salary_df.dropna(subset=["Salary_Num"])

        if not salary_df.empty:
            salary_count = salary_df["Salary_Num"].value_counts().sort_index()

            fig = px.bar(
                x=salary_count.index,
                y=salary_count.values,
                labels={
                    "x": "Salary (LPA)",
                    "y": "Number of Jobs"
                },
                title="Salary Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No salary data available.")

        st.subheader("🛠 Top 10 In-Demand Skills")

        skills_df = df.copy()
        skills_df["Skills"] = skills_df["Skills"].fillna("")

        skills_list = []
        for skills_val in skills_df["Skills"]:
            for skill in skills_val.split(","):
                skill = skill.strip()
                if skill:
                    skills_list.append(skill)

        if skills_list:
            skills_count = (
                pd.Series(skills_list)
                .value_counts()
                .head(10)
                .rename_axis("Skill")
                .reset_index(name="Jobs")
            )

            fig_skills = px.pie(
                skills_count,
                names="Skill",
                values="Jobs",
                hole=0.45,
                title="Top 10 In-Demand Skills"
            )
            fig_skills.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )
            st.plotly_chart(fig_skills, use_container_width=True)
        else:
            st.info("No skills data available.")

        st.subheader("📈 Job Posting Trend")
        trend_df = df.copy()
        trend_df["Posted Date"] = pd.to_datetime(
            trend_df["Posted Date"],
            errors="coerce"
        )
        trend_df = trend_df.dropna(subset=["Posted Date"])

        if not trend_df.empty:
            trend_count = (
                trend_df.groupby("Posted Date")
                .size()
                .reset_index(name="Jobs")
            )

            fig_trend = px.line(
                trend_count,
                x="Posted Date",
                y="Jobs",
                markers=True,
                title="Job Posting Trend"
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No posting date data available.")

    with tab3:
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Filtered Jobs (CSV)",
            data=csv,
            file_name="filtered_jobs.csv",
            mime="text/csv"
        )

        st.subheader("📋 Job Listings")

        search_job = st.text_input(
            "🔍 Search Job Listings",
            placeholder="Search by Job Title, Company or Skills..."
        )

        display_df = df.copy()

        if search_job:
            display_df = display_df[
                display_df["Job Title"].str.contains(search_job, case=False, na=False) |
                display_df["Company"].str.contains(search_job, case=False, na=False) |
                display_df["Skills"].str.contains(search_job, case=False, na=False)
            ]

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("📄 Job Details")

        for _, row in display_df.iterrows():
            with st.expander(f"💼 {row['Job Title']} | {row['Company']}"):
                detail_col1, detail_col2 = st.columns(2)

                with detail_col1:
                    st.write("📍 **Location:**", row["Location"])
                    st.write("💰 **Salary:**", row["Salary"])
                    st.write("👨‍💻 **Experience:**", row["Experience"])

                with detail_col2:
                    st.write("🛠 **Skills:**", row["Skills"])
                    st.write(
                        "📅 **Posted Date:**",
                        str(row["Posted Date"].date()) if pd.notna(row["Posted Date"]) else "N/A"
                    )
                    st.write("🌐 **Source:**", row["Source"])

    with tab4:
        st.subheader("🎯 Job Recommendation System")

        st.write("Enter your skills and we'll recommend the best matching jobs.")

        st.subheader("📄 Upload Your Resume")

        uploaded_resume = st.file_uploader(
            "Upload your resume (PDF)",
            type=["pdf"]
        )

        user_skills = []

        if uploaded_resume is not None:
            resume_text = extract_text_from_pdf(uploaded_resume)
            resume_skills = extract_skills(resume_text)

            if resume_skills:
                st.success("Resume analyzed successfully!")
                st.write("Detected Skills:", ", ".join(resume_skills))
                user_skills = resume_skills
            else:
                st.warning("No matching skills detected in the resume.")

        if not user_skills:
            skills_input = st.text_input(
                "Enter your skills (comma separated)",
                placeholder="Python, SQL, Machine Learning"
            )

            if skills_input:
                user_skills = [
                    skill.strip().lower()
                    for skill in skills_input.split(",")
                    if skill.strip()
                ]

        if user_skills:
            recommended = recommend_jobs(
                df,
                user_skills,
                top_n=10
            )

            if recommended.empty:
                st.warning("No matching jobs found.")
            else:
                st.success(f"Found {len(recommended)} recommended jobs!")

               

                available_columns = recommended.columns.tolist()
                display_columns = [
                    col for col in [
                        "Job Title",
                        "Company",
                        "Location",
                        "Skills",
                        "Match Score",
                        "Match %"
                    ] if col in available_columns
                ]

                st.dataframe(
                    recommended[display_columns] if display_columns else recommended,
                    use_container_width=True,
                    hide_index=True
                )

    with tab5:
        st.subheader("💰 Salary Prediction")
        st.write("Enter your details to estimate your annual salary.")

        experience = st.number_input(
            "Years of Experience",
            min_value=0,
            max_value=30,
            value=0,
            step=1
        )

        skills_count = st.number_input(
            "Number of Skills",
            min_value=1,
            max_value=30,
            value=1,
            step=1
        )

        job_role_name = st.selectbox(
            "Job Role",
            [
                "Data Analyst",
                "Data Scientist",
                "ML Engineer",
                "Software Engineer"
            ]
        )

        job_role_map = {
            "Data Analyst": 1,
            "Data Scientist": 2,
            "ML Engineer": 3,
            "Software Engineer": 4
        }

        job_role = job_role_map[job_role_name]

        if st.button("Predict Salary"):
            predicted_salary = predict_salary(
                experience,
                skills_count,
                job_role
            )

            salary_lpa = predicted_salary / 100000
            monthly_salary = predicted_salary / 12

            st.success(
                f"💰 Predicted Annual Salary: ₹{predicted_salary:,.2f}"
            )

            st.info(
                f"📊 Estimated Package: {salary_lpa:.2f} LPA"
            )

            st.write(
                f"📅 Estimated Monthly Salary: **₹{monthly_salary:,.2f}**"
            )

            st.caption(
                f"Based on {experience} years of experience, "
                f"{skills_count} skills, and the selected job role."
            )

            if salary_lpa < 5:
                salary_level = "Entry Level"
            elif salary_lpa < 10:
                salary_level = "Mid Level"
            else:
                salary_level = "High Level"

            st.write(f"💼 Salary Level: **{salary_level}**")

            if salary_lpa < 5:
                career_tip = "Build more projects and strengthen your technical skills."
            elif salary_lpa < 10:
                career_tip = "Focus on advanced skills and industry-level projects to reach higher packages."
            else:
                career_tip = "Strong salary potential! Focus on specialization and leadership skills."

            st.info(f"🚀 Career Tip: {career_tip}")

            if experience >= 2 and skills_count >= 4:
                confidence = "High"
            elif experience >= 1 and skills_count >= 2:
                confidence = "Medium"
            else:
                confidence = "Low"

            st.write(f"🤖 Input Strength: **{confidence}**")

            st.write("📈 Salary Growth Indicator")

            progress_value = min(salary_lpa / 20, 1.0)
            st.progress(progress_value)

            progress_percent = progress_value * 100

            st.caption(
                f"Current predicted package is {progress_percent:.1f}% of the 20 LPA reference scale."
            )

            target_lpa = 20
            gap_lpa = max(target_lpa - salary_lpa, 0)

            if gap_lpa > 0:
                st.write(
                    f"🎯 Gap to {target_lpa} LPA: **{gap_lpa:.2f} LPA**"
                )
            else:
                st.success("🎯 You have reached or exceeded the 20 LPA reference target!")

            if salary_lpa < target_lpa:
                growth_needed = ((target_lpa - salary_lpa) / salary_lpa) * 100

                st.write(
                    f"📈 Growth Needed to Reach {target_lpa} LPA: "
                    f"**{growth_needed:.1f}%**"
                )

            if salary_lpa >= 20:
                target_status = "Target Achieved"
            elif salary_lpa >= 15:
                target_status = "Very Close to Target"
            elif salary_lpa >= 10:
                target_status = "Good Progress"
            else:
                target_status = "Keep Building Skills"

            st.write(f"🏆 Target Status: **{target_status}**")

            if salary_lpa < 10:
                next_milestone = 10
            elif salary_lpa < 15:
                next_milestone = 15
            elif salary_lpa < 20:
                next_milestone = 20
            else:
                next_milestone = 25

            milestone_gap = next_milestone - salary_lpa

            st.write(
                f"🚩 Next Milestone: **{next_milestone} LPA** "
                f"(Need {milestone_gap:.2f} LPA more)"
            )

            milestone_progress = min(salary_lpa / next_milestone, 1.0)

            st.write("🚀 Progress to Next Milestone")
            st.progress(milestone_progress)

            st.caption(
                f"You are {milestone_progress * 100:.1f}% of the way "
                f"to the {next_milestone} LPA milestone."
            )

            if skills_count < 3:
                skill_tip = "Add more job-relevant technical skills to strengthen your profile."
            elif skills_count < 6:
                skill_tip = "Good skill base. Focus on advanced and specialized skills."
            else:
                skill_tip = "Strong skill portfolio. Focus on depth and real-world experience."

            st.markdown("---")
            st.subheader("🎯 Personalized Career Guidance")

            st.info(f"🧠 Skill Recommendation: {skill_tip}")

            if experience < 1:
                experience_tip = "Focus on internships, projects, and entry-level opportunities."
            elif experience < 3:
                experience_tip = "Build strong project experience and take ownership of real-world tasks."
            elif experience < 5:
                experience_tip = "Focus on specialization, advanced projects, and higher-impact roles."
            else:
                experience_tip = "Target senior roles and strengthen leadership and system-design skills."

            st.info(f"💼 Experience Recommendation: {experience_tip}")

            if salary_lpa < 10:
                next_action = "Build 2–3 strong industry projects and improve advanced technical skills."
            elif salary_lpa < 15:
                next_action = "Focus on specialization, interview preparation, and high-impact projects."
            elif salary_lpa < 20:
                next_action = "Target product-based companies and strengthen system design and advanced skills."
            else:
                next_action = "Target senior and specialized roles with higher responsibility."

            st.success(f"✅ Recommended Next Action: {next_action}")

        st.caption(
            "⚠️ Salary predictions are estimates generated by the ML model "
            "and may vary based on company, location, skills, and market conditions."
        )

except psycopg2.OperationalError as e:
    st.error(f"❌ Could not connect to the database. Please check your connection settings.\n\n{e}")
except Exception as e:
    st.error(f"❌ An unexpected error occurred: {e}")
finally:
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()