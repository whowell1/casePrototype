import os
import pyautogui
import keyboard
from datetime import datetime
# Define the directory path
directory = os.path.join(os.path.expanduser("~"), "Desktop", "investigations")
# Create the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)
# Define the target key
target_key = 'a'
# Define a flag to keep track if the key is pressed
key_pressed = False
# Function to take a screenshot
def take_screenshot():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(directory, f'screenshot_{timestamp}.png')
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print("Screenshot saved as:", filename)
# Function to check for the key press
def check_key(event):
    global key_pressed
    if event.event_type == keyboard.KEY_DOWN and event.name == target_key:
        key_pressed = True
    elif event.event_type == keyboard.KEY_UP and event.name == target_key:
        key_pressed = False
    elif key_pressed and event.event_type == keyboard.KEY_DOWN and event.name == 'q':
        take_screenshot()
# Start the listener
keyboard.on_press(check_key)
# Keep the script running
keyboard.wait('esc')












