import psycopg2

while True:

    try:
        conn = psycopg2.connect(
            host="localhost",
            database="ai_job_market",
            user="postgres",
            password="root",
            port="5432"
        )

        cursor = conn.cursor()

        print("\n" + "=" * 60)
        print("      AI Job Market Intelligence Platform")
        print("=" * 60)

        print("1. Search by Job Title")
        print("2. Search by Company")
        print("3. Search by Location")
        print("4. Show All Jobs")
        print("5. Job Statistics")
        print("6. Search by Skills")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        jobs = []


        if choice == "1":

            keyword = input("\nEnter Job Title: ")

            cursor.execute("""
                SELECT * FROM jobs
                WHERE LOWER(job_title) LIKE LOWER(%s)
                ORDER BY job_id;
            """, (f"%{keyword}%",))

            jobs = cursor.fetchall()


        elif choice == "2":

            keyword = input("\nEnter Company Name: ")

            cursor.execute("""
                SELECT * FROM jobs
                WHERE LOWER(company) LIKE LOWER(%s)
                ORDER BY job_id;
            """, (f"%{keyword}%",))

            jobs = cursor.fetchall()


        elif choice == "3":

            keyword = input("\nEnter Location: ")

            cursor.execute("""
                SELECT * FROM jobs
                WHERE LOWER(location) LIKE LOWER(%s)
                ORDER BY job_id;
            """, (f"%{keyword}%",))

            jobs = cursor.fetchall()

   
        elif choice == "4":

            cursor.execute("""
                SELECT *
                FROM jobs
                ORDER BY job_id;
            """)

            jobs = cursor.fetchall()


        elif choice == "5":

            cursor.execute("SELECT COUNT(*) FROM jobs;")
            total_jobs = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT company) FROM jobs;")
            total_companies = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT location) FROM jobs;")
            total_locations = cursor.fetchone()[0]

            print("\n" + "=" * 50)
            print("              JOB STATISTICS")
            print("=" * 50)
            print(f"Total Jobs      : {total_jobs}")
            print(f"Total Companies : {total_companies}")
            print(f"Total Locations : {total_locations}")
            print("=" * 50)

            cursor.close()
            conn.close()

            input("\nPress Enter to return to the menu...")
            continue


        elif choice == "6":

            keyword = input("\nEnter Skill: ")

            cursor.execute("""
                SELECT *
                FROM jobs
                WHERE LOWER(skills) LIKE LOWER(%s)
                ORDER BY job_id;
            """, (f"%{keyword}%",))

            jobs = cursor.fetchall()


        elif choice == "7":

            cursor.close()
            conn.close()

            print("\nThank you for using AI Job Market Intelligence Platform!")
            break

        else:

            print("\n❌ Invalid Choice!")

            cursor.close()
            conn.close()

            input("\nPress Enter to continue...")
            continue

  
        print("\n" + "=" * 60)
        print(f"Jobs Found : {len(jobs)}")
        print("=" * 60)

        if len(jobs) == 0:

            print("\nNo matching jobs found.")

        else:

            for job in jobs:

                print("\n" + "=" * 60)
                print(f"Job ID       : {job[0]}")
                print(f"Job Title    : {job[1]}")
                print(f"Company      : {job[2]}")
                print(f"Location     : {job[3]}")
                print(f"Salary       : {job[4]}")
                print(f"Experience   : {job[5]}")
                print(f"Skills       : {job[6]}")
                print(f"Description  : {job[7]}")
                print(f"Posted Date  : {job[8]}")
                print(f"Source       : {job[9]}")
                print(f"Job URL      : {job[10]}")
                print("=" * 60)

        cursor.close()
        conn.close()

        input("\nPress Enter to return to the menu...")

    except Exception as e:

        print("\n❌ Database Error!")
        print(e)
        break
    