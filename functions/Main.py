import os
import pygetwindow as gw
import datetime
import sqlite3
# Set web files folder
#comment

def cp(wname):
    conn = sqlite3.connect('./db/local_database.db')
    #create_table(conn)
    hostname, username = get_system_details()
    print(wname)
    print(hostname)
    print(username)
    current_window_name=wname
    insert_data(conn, current_window_name, hostname, username)

# Function to insert data into database
def insert_data(conn, window_name, hostname, username):
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO UserActivity (System_Name, User_Name, Active_Application, DateTime_Stamp)
                      VALUES (?, ?, ?, ?)''', (hostname, username,window_name, datetime.datetime.now()))
    conn.commit()
# Function to get current system details
def get_system_details():
    hostname = os.environ['COMPUTERNAME']
    username = os.environ['USERNAME']
    return hostname, username

