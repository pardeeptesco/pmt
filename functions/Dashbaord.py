import sqlite3
from datetime import datetime


def calculate_volume(today_date):
    # Connect to the SQLite database for volume calculation
    conn = sqlite3.connect('./db/aht/activities_log.db')
    cursor = conn.cursor()

    # Calculate sum of volumes for today's date
    cursor.execute("SELECT SUM(volume) FROM activities_log WHERE DATE(date_time) = ?", (today_date,))
    volume_result = cursor.fetchone()[0]
    if volume_result is None:
        volume_result = 0  # If there are no records for today, set volume to 0

    # Close database connection
    conn.close()

    return volume_result

def calculate_total_hours():
    # Connect to the SQLite database
    conn = sqlite3.connect('./db/local_database.db')
    cursor = conn.cursor()
    
    # Get current date
    today_date = datetime.now().date()
    
    # Get largest and lowest datetime stamps for today
    cursor.execute("SELECT MAX(DateTime_Stamp), MIN(DateTime_Stamp) FROM UserActivity WHERE DATE(DateTime_Stamp) = ?", (today_date,))
    result = cursor.fetchone()
    
    # Check if result is not None
    if result is not None and result[0] is not None and result[1] is not None:
        # Convert fetched values to datetime objects
        largest_datetime = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S.%f')
        lowest_datetime = datetime.strptime(result[1], '%Y-%m-%d %H:%M:%S.%f')
        
        # Calculate total number of hours
        total_hours = round((largest_datetime - lowest_datetime).total_seconds() / 3600, 2)
    else:
        total_hours = 0.0  # No records found, set total_hours to 0
    
    # Close database connection
    conn.close()

    return total_hours

def calculate_activity_count(today_date):
    # Connect to the SQLite database for activity count
    conn = sqlite3.connect('./db/activityPlanner.db')
    cursor = conn.cursor()

    # Count planned activities for today's date
    cursor.execute("SELECT COUNT(*) FROM planned_activities WHERE DATE(date_time) = ?", (today_date,))
    activity_count = cursor.fetchone()[0]

    # Close database connection
    conn.close()

    return activity_count


