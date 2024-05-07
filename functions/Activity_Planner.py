import sqlite3
from sqlite3 import Error


# Function to save planned activities into the database
def save_activity_planned(start_date, end_date, start_time, end_time, activity):
    try:
        conn = sqlite3.connect('./db/activityPlanner.db')
        c = conn.cursor()

        # Insert data into the database
        c.execute("INSERT INTO planned_activities (start_date, end_date, start_time, end_time, activity) VALUES (?, ?, ?, ?, ?)",
                  (start_date, end_date, start_time, end_time, activity))

        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()



# Function to fetch activity planner records from the database
def fetch_activity_planner_records():
    try:
        conn = sqlite3.connect('./db/activityPlanner.db')
        c = conn.cursor()
        c.execute("SELECT * FROM planned_activities")
        records = c.fetchall()
        return records
    except Error as e:
        print(e)
    finally:
        conn.close()

# Expose fetchActivityPlannerRecords function to JavaScript

# Function to get activity list from the database
def getActivityList():
    try:
        conn = sqlite3.connect('./db/local_database.db')
        cursor = conn.cursor()

        # Execute the query to select all rows from the activitylist table
        cursor.execute("SELECT * FROM activitylist")

        # Fetch all rows
        rows = cursor.fetchall()

        # Prepare data to return
        activity_list = []
        for row in rows:
            activity_list.append({
                'ActivityName': row[0],
                'ActivityCategory': row[1]
            })

        return {'activityList': activity_list}
    except Error as e:
        print(e)
    finally:
        conn.close()

