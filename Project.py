import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial 
import threading
import time
import imutils

# Load the video file
stream = cv2.VideoCapture("Runout.mp4")

def play(speed):
    print(f"You clicked on. Speed is {speed}")
    
    # Get current frame position and adjust by speed
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    # Read the next frame from the video
    grabbed, frame = stream.read()
    
    if not grabbed:
        print("End of video.")
        return
    
    # Resize the frame
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    
    # Convert the frame from BGR (OpenCV default) to RGB (required for Tkinter)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Convert the frame to a PIL image, then to a Tkinter image
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    
    # Update the canvas with the new frame
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)

def pending(decision):
    # Display the 'Decision Pending' image
    frame = cv2.cvtColor(cv2.imread("decision.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)
    
    time.sleep(1.5)
    
    # Display either the 'Out' or 'Not Out' image
    if decision == 'Out':
        decision_img = "out.png"
    else:
        decision_img = "not out.png"
        
    frame = cv2.cvtColor(cv2.imread(decision_img), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)

# Handle the 'Out' decision
def Out():
    thread = threading.Thread(target=pending, args=("Out",))
    thread.daemon = 1
    thread.start()
    print('Player is Out')

# Handle the 'Not Out' decision
def notOut():
    thread = threading.Thread(target=pending, args=("NotOut",))
    thread.daemon = 1
    thread.start()
    print('Player is Not Out')

# Set the width and height of the main window
SET_WIDTH = 700
SET_HEIGHT = 400

# Initialize the Tkinter window
window = tk.Tk()
window.title("THIRD UMPIRE DECISION SYSTEM")

# Load a background image (e.g., "ground.png")
cv2_img = cv2.cvtColor(cv2.imread("ground.png"), cv2.COLOR_BGR2RGB)
canvas = tk.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2_img))
image_on_canvas = canvas.create_image(0, 0, anchor=tk.NW, image=photo)
canvas.pack()

# Buttons for playback control
btn_fast_backward = tk.Button(window, text="<< Previous (Fast)", width=50, command=partial(play, -25))
btn_fast_backward.pack()

btn_slow_backward = tk.Button(window, text="<< Previous (Slow)", width=50, command=partial(play, -2))
btn_slow_backward.pack()

btn_fast_forward = tk.Button(window, text="Next (Fast) >>", width=50, command=partial(play, 25))
btn_fast_forward.pack()

btn_slow_forward = tk.Button(window, text="Next (Slow) >>", width=50, command=partial(play, 3))
btn_slow_forward.pack()

btn_out = tk.Button(window, text="OUT", width=50, command=Out)
btn_out.pack()

btn_not_out = tk.Button(window, text="NOT OUT", width=50, command=notOut)
btn_not_out.pack()

# Run the Tkinter event loop
window.mainloop()
