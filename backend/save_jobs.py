import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="ai_job_market",
        user="postgres",
        password="root",
        port="5432"
    )

    print("✅ Database Connected!")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO jobs
    (
        job_title,
        company,
        location,
        salary,
        experience,
        skills,
        job_description,
        posted_date,
        source,
        job_url
    )
    VALUES
    (
        'Python Developer',
        'Real Python',
        'Remote',
        'Not Mentioned',
        'Not Mentioned',
        'Python',
        'Scraped from website',
        CURRENT_DATE,
        'RealPython',
        'https://realpython.com'
    )
    """)

    conn.commit()

    print("✅ Job Saved Successfully!")

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Connection Failed!")
    print(e)