import psycopg2

try:
    conn = psycopg2.connect(
        host="db.bxjgyyyjwmwpuixbkwhl.supabase.co",
        database="postgres",
        user="postgres",
        password="arun23242526!",
        port="5432",
        sslmode="require",
        connect_timeout=10
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