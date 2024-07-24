# This is the main code. Before start, run CamSim....py (Optional)
# You can find instructions in hackster.io
# Remember to put both (the .h5 and .txt files in the same folder!)
# Before running remember to replace camera port and paths (example given)
# For this to run install these libraries :
# pip install teachable-machine
# pip install opencv-python
# pip install pynput
 
from teachable_machine import TeachableMachine
from pynput.keyboard import Key, Controller
import cv2
import numpy as np
import io
from PIL import Image
import time

countdown_seconds = 30 # If you need more time before the code starts, change this.

camera_port = 2 # !!! REPLACE this with your accual camera port. You can check with the cameraPortTest.py code

# !!! REPLACE these paths with the absolute paths to your model and labels files
model_path = "E:\\MANI FAILI\\Programming-Graphics-Games\\MD-pervasive-ai-dev-contest\\Developement\\AmongUs_model\\keras_model.h5"
labels_path = "E:\\MANI FAILI\\Programming-Graphics-Games\\AMD-pervasive-ai-dev-contest\\Developement\\AmongUs_model\\labels.txt"

keyboard = Controller()

#Countdown timer
for seconds_remaining in range(countdown_seconds, 0, -1):
    print(f"Starting in {seconds_remaining} second{'s' if seconds_remaining > 1 else ''}")
    time.sleep(1)

print("Countdown complete. Starting code!")

model = TeachableMachine(model_path=model_path, labels_file_path=labels_path)

# Open the camera stream
cap = cv2.VideoCapture(camera_port)

while True:
    _, img = cap.read()

    # Convert the image (numpy array) to bytes
    img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
    
    # Classify the image
    result = model.classify_image(io.BytesIO(img_bytes))

    # Extract classification results
    class_index = result["class_index"]
    class_name = result["class_name"]
    class_confidence = result["class_confidence"]
    predictions = result["predictions"]

    # Print prediction and confidence score
    print("Class Index:", class_index)
    print("Class Confidence:", class_confidence)
    print("Predictions:", predictions)

    # Show the image in a window
    cv2.imshow("Webcam Image", img)

    if class_index == 0:
        print("Normal")
    if class_index == 1:
        print("Left")
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    if class_index == 2:
        print("Right")
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    if class_index == 3:
        print("Rotate")
        keyboard.press(Key.up)
        keyboard.release(Key.up)

    time.sleep(0.5)

    # Listen to the keyboard for presses
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the Esc key on your keyboard
    if keyboard_input == 27:
        break

cap.release()
cv2.destroyAllWindows()