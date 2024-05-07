import sqlite3
import time
import os

# Construct the database file path using os.path.join()
db_file_path = os.path.join('./db', 'aht', 'activities.db')

# Function to fetch activity options from SQLite database
def get_activity_options():
    try:
        conn = sqlite3.connect(db_file_path)
        c = conn.cursor()
        c.execute("SELECT name FROM activities")
        options = c.fetchall()
        conn.close()
        return [option[0] for option in options]
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return []

# Function to add new activity entry to the table
def add_activity_entry(activity_name):
    conn = sqlite3.connect('./db/aht/activities_log.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*), stopped FROM activities_log WHERE name = ?", (activity_name,))
    count, stopped_value = c.fetchone()
    if count == 0:
        c.execute("INSERT INTO activities_log (name, start_time, end_time, total_time, stopped, volume) VALUES (?, ?, ?, ?, ?, ?)", (activity_name, int(time.time()), 0, 0, 0, 0))
    elif stopped_value != 2:
        c.execute("UPDATE activities_log SET stopped = ? WHERE name = ?", (0, activity_name))
    conn.commit()
    conn.close()

# Function to pause activity 
def pause_activity_entry(activity_name):
    conn = sqlite3.connect('./db/aht/activities_log.db')
    c = conn.cursor()
    c.execute("UPDATE activities_log SET stopped = 1 WHERE stopped = 0 AND name = ?", (activity_name,))
    conn.commit()
    conn.close()

# Function to end the timer
def stop_activity(activity_name, volume):
    conn = sqlite3.connect('./db/aht/activities_log.db')
    c = conn.cursor()
    
    current_time = time.strftime('%Y-%m-%d %H:%M:%S.') + "{:06d}".format(int(time.time() * 1000000) % 1000000)
    
    c.execute("UPDATE activities_log SET end_time = ?, total_time = total_time + (CAST(strftime('%s', 'now') AS INTEGER) - start_time), stopped = 2, volume = ?, date_time = ? WHERE end_time = 0 AND name = ?", (int(time.time()), volume, current_time, activity_name))
    
    conn.commit()
    conn.close()

# Function to fetch active activities
def fetch_active_activities():
    conn = sqlite3.connect('./db/aht/activities_log.db')
    c = conn.cursor()
    c.execute("SELECT * FROM activities_log")
    active_activities = c.fetchall()
    conn.close()
    return active_activities

# Start (this will block and keep the GUI alive)




# eel.start('AHT_template.html', size=(850, 450), port=3001)
