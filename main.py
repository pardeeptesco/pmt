import eel
import subprocess
import os

import webbrowser
import os
from PIL import Image
from pystray import MenuItem, Icon, Menu
import threading
from datetime import datetime
import subprocess


from functions.Main import cp
from functions.AHT_Calculator import (get_activity_options, add_activity_entry, pause_activity_entry, stop_activity,fetch_active_activities)
from functions.Dashbaord import (calculate_activity_count,calculate_total_hours, calculate_volume)
from functions.Activity_Planner import (getActivityList, fetch_activity_planner_records, save_activity_planned)
# Initialize Eel
eel.init('web')

myprocess = None
myprocess= subprocess.Popen(["python", "capture.py"])


# ----------***-----------MAIN Expose Functions Starts Here----------***-------------
# Define a global variable to hold the process

# Define a function to launch the AHT script
@eel.expose
def launch_aht():
    # Check if the AHT script exists
    eel.show("AHT_template.html")

# Define a function to launch the Activity Planner script
@eel.expose
def launchaplanner():
    # Check if the Activity Planner script exists
    eel.show("Activity_template.html")
# Define a function to toggle the button state
@eel.expose
def toggle_slider_state(state):
    global myprocess  # Declare myprocess as a global variable
    print("Button state:", state)
    if state:
        # Terminate the process if it exists
        if myprocess:
            myprocess.terminate()
        cp('PrivateModeOn')  # Assuming cp is a function defined elsewhere
    else:
        # Start the process
        myprocess = subprocess.Popen(["python", "capture.py"])
        cp('PrivateModeOFF')  # Assuming cp is a function defined elsewhere
# ----------***-----------MAIN Expose Functions Ends Here----------***-------------




# ----------***-----------AHT Expose Functions Starts Here----------***-------------

@eel.expose
def fetch_activity_options():
    return get_activity_options()

@eel.expose
def add_activity_entry_to_table(activity_name):
    add_activity_entry(activity_name)

@eel.expose
def pause_activity_entry_to_table(activity_name):
    pause_activity_entry(activity_name)

@eel.expose
def stop_activity_entry_to_table(activity_name, volume):
    stop_activity(activity_name, volume)

@eel.expose
def fetch_active_activities_from_db():
    return fetch_active_activities()

# ----------***-----------AHT Expose Functions Ends Here----------***-------------



# ----------***-----------Dashboard Expose Functions Starts Here----------***-------------

@eel.expose
def dashboardData():
    today_date = datetime.now().date()
    total_hours = calculate_total_hours()
    volume_result = calculate_volume(today_date)
    activity_count = calculate_activity_count(today_date) 

    final_data = {
      "total_hours": total_hours,
      "break_hours": 3.5, # currently no logic passing dummy one
      "activities_count": activity_count,
      "volume": volume_result
    }
    
    return final_data

# ----------***-----------Dashboard Expose Functions Ends Here----------***-------------

# ----------***-----------Activity Manager Expose Functions Ends Here----------***-------------


@eel.expose
def get_activity_list():
    return getActivityList()

@eel.expose
def fetchActivityPlannerRecords():
    return fetch_activity_planner_records()

@eel.expose
def saveActivityPlanned(start_date, end_date, start_time, end_time, activity):
    save_activity_planned(start_date, end_date, start_time, end_time, activity)


# ----------***-----------Activity Manager Expose Functions Ends Here----------***-------------



# ----------***-----------Project Setup----------***-------------




def launch_app(icon, item):
    launchMainApp()

def launch_dashboard():
    eel.show("Dashboard.html")

def launch_activity_planner():
    eel.show("Activity_template.html")


def quit_callback(icon, item):
    icon.stop()

def on_quit(icon, item):
    print("Quitting...")

def launchMainApp():
    eel.show("index.html")

def backgroundApp():
    eel.start('index.html',disable_cache=True, mode="chrome", size=(370, 500), position=(100, 100), callback=on_quit)



def open_help(self):
    webbrowser.open("https://help.ourtesco.com")


if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load the icon image from the root of the project
    icon_image_path = os.path.join(script_dir, "web/SRCPNG.png")
    icon_image = Image.open(icon_image_path)

    # Create a system tray icon
    icon = Icon("Python Eel Tray App", icon_image, menu=Menu
                (
                    # MenuItem('PMT CLIENT', launchMainApp),
                    MenuItem('DASHBOARD', launch_dashboard), 
                    MenuItem("MULTI-ROLE", open_help),
                    MenuItem("Help", open_help),
                    MenuItem('Exit', quit_callback)
                    ))

    # Start the icon in a separate thread
    threading.Thread(target=icon.run).start()

    # Start Eel in the main thread
    backgroundApp()


    
