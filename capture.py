# import necessary libraries
import os
# import pygetwindow as gw
import datetime
import sqlite3
import time
import re
#comment
def formats(input_string):
   
    if input_string=="" or input_string==None:
        return "Application Not Captured"
   
    output_string = input_string.split('|')[-1].strip()

   
    if 'outlook' in output_string.lower():
       
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        
        emails = re.findall(email_pattern, output_string)
        
    #    removing emails
        if emails:
            email = emails[0]
            output_string = output_string.replace(email, '')
            return output_string.strip() 
        else:
            return output_string.strip() 
        
    
    return output_string

# capture function
def capture():
    conn = sqlite3.connect('./db/local_database.db')
    #create_table(conn)

    prev_window_name = ''
    prev_timestamp = None

    while True:
        current_window_name = get_active_window_name()
        if current_window_name != prev_window_name:
            hostname, username = get_system_details()
            insert_data(conn, current_window_name, hostname, username)
            prev_window_name = current_window_name
            prev_timestamp = datetime.datetime.now()
                
        time.sleep(1)
# Function to get active application window name
def get_active_window_name():
    return "Test"


# Function to insert data into database
def insert_data(conn, window_name, hostname, username):
    cursor = conn.cursor()
    window_name=formats(window_name)
    cursor.execute('''INSERT INTO UserActivity (System_Name, User_Name, Active_Application, DateTime_Stamp)
                      VALUES (?, ?, ?, ?)''', (hostname, username,window_name, datetime.datetime.now()))
    conn.commit()

# Function to create database table
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS UserActivity (
                    System_Name TEXT,
                    User_Name TEXT,
                    Active_Application TEXT,
                    DateTime_Stamp DATETIME''')
    conn.commit()
# Function to get current system details
def get_system_details():
    hostname = os.environ['COMPUTERNAME']
    username = os.environ['USERNAME']
    return hostname, username



capture()
