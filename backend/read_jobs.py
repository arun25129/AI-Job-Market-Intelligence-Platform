import psycopg2

try:
    # ==========================
    # Connect to PostgreSQL Database
    # ==========================
    conn = psycopg2.connect(
        host="localhost",
        database="ai_job_market",
        user="postgres",
        password="root",      # Change if your password is different
        port="5432"
    )

    print("\n✅ Database Connected Successfully!")

    cursor = conn.cursor()

    # ==========================
    # Search Job by Keyword
    # ==========================
    keyword = input("\n🔍 Enter Job Keyword: ")

    cursor.execute("""
        SELECT *
        FROM jobs
        WHERE LOWER(job_title) LIKE LOWER(%s)
        ORDER BY job_id;
    """, (f"%{keyword}%",))

    jobs = cursor.fetchall()

    print("\n" + "=" * 70)
    print(f"🎯 Total Jobs Found: {len(jobs)}")
    print("=" * 70)

    if not jobs:
        print("\n❌ No jobs found for this keyword.")
    else:
        for job in jobs:
            print("\n" + "=" * 70)
            print(f"🆔 Job ID        : {job[0]}")
            print(f"💼 Job Title     : {job[1]}")
            print(f"🏢 Company       : {job[2]}")
            print(f"📍 Location      : {job[3]}")
            print(f"💰 Salary        : {job[4]}")
            print(f"📈 Experience    : {job[5]}")
            print(f"🛠 Skills        : {job[6]}")
            print(f"📝 Description   : {job[7]}")
            print(f"📅 Posted Date   : {job[8]}")
            print(f"🌐 Source        : {job[9]}")
            print(f"🔗 Job URL       : {job[10]}")
            print("=" * 70)

    # ==========================
    # Close Database Connection
    # ==========================
    cursor.close()
    conn.close()

    print("\n✅ Database Connection Closed Successfully!")

except Exception as e:
    print("\n❌ Error!")
    print(e)