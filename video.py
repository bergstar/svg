import os
import time
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configure the headless browser
options = Options()
options.headless = True
options.add_argument("--disable-gpu")

# Initialize the headless browser
browser = webdriver.Chrome(options=options)

# Load the SVG animation URL
animation_url = 'http://localhost:5000/svg'  # Replace with your Flask app URL
browser.get(animation_url)

# Set the browser window size to match the SVG size
browser.set_window_size(400, 600)

# Parameters for capturing animation frames
frame_rate = 60  # Frame rate for the video (frames per second)
duration = 10     # Duration of the video in seconds

# Initialize the video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter('animation.avi', fourcc, frame_rate, (400, 600))

# Capture animation frames
start_time = time.time()
while time.time() - start_time < duration:
    # Capture a screenshot of the current frame
    browser.save_screenshot('frame.png')

    # Load the screenshot as an OpenCV image
    frame = cv2.imread('frame.png')

    # Write the frame to the video file
    video_writer.write(frame)

    # Wait for the next frame
    time.sleep(1 / frame_rate)

# Cleanup
video_writer.release()
browser.quit()
os.remove('frame.png')
