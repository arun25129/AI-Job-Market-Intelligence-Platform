import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="ai_job_market",
        user="postgres",
        password="root",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs;")

    rows = cursor.fetchall()

    print("Jobs Table Data:\n")

    for row in rows:
        print(row)

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Connection failed!")
    print(e)