import time
import PySimpleGUI as sg
import cv2
import pygame
import io
from teachable_machine import TeachableMachine
from PIL import Image
import numpy as np
from pynput.keyboard import Key, Controller
import pyttsx3
import speech_recognition as sr
import pyaudio

model_path = "image_model/ai_model.h5"
labels_path = "image_model/labels.txt"

model = TeachableMachine(model_path=model_path, labels_file_path=labels_path)

countdown_seconds = 10

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 120)
volume = engine.getProperty('volume')
engine.setProperty('volume',0.8)

pygame.mixer.init()

keyboard = Controller()

recognizer = sr.Recognizer()

stop = False

def listen_for_stop():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening...")
    while True:
      audio = r.listen(source)
      try:
        text = r.recognize_google(audio)
        print(text)
        if "stop" in text.lower():
          print("Stop command detected!")
          stop = True
          break
      except sr.UnknownValueError:
        print("Could not understand audio")
      except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def listen_for_drop():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening...")
    while True:
      audio = r.listen(source)
      try:
        text = r.recognize_google(audio)
        print(text)
        if "drop" in text.lower():
          print("Drop command detected!")
          keyboard.press(Key.space)
          keyboard.release(Key.space)
          break
      except sr.UnknownValueError:
        print("Could not understand audio")
      except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def listen_for_action():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening...")
    while True:
      audio = r.listen(source)
      try:
        text = r.recognize_google(audio)
        print(text)
        if "action" in text.lower():
          print("Action command detected!")
          keyboard.press("r")
          keyboard.release("r")
          keyboard.press("q")
          keyboard.release("q")
          break
      except sr.UnknownValueError:
        print("Could not understand audio")
      except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def listen_for_speed():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening...")
    while True:
      audio = r.listen(source)
      try:
        text = r.recognize_google(audio)
        print(text)
        if "action" in text.lower():
          print("Action command detected!")
          keyboard.press("w")
          keyboard.release("s")
          break
      except sr.UnknownValueError:
        print("Could not understand audio")
      except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def listen_for_brakes():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening...")
    while True:
      audio = r.listen(source)
      try:
        text = r.recognize_google(audio)
        print(text)
        if "action" in text.lower():
          print("Action command detected!")
          keyboard.press("s")
          keyboard.release("w")
          break
      except sr.UnknownValueError:
        print("Could not understand audio")
      except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def listen_for_boost():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening...")
    while True:
      audio = r.listen(source)
      try:
        text = r.recognize_google(audio)
        print(text)
        if "action" in text.lower():
          print("Action command detected!")
          keyboard.press(Key.shift)
          keyboard.release(Key.shift)
          break
      except sr.UnknownValueError:
        print("Could not understand audio")
      except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def listen_for_jump():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening...")
    while True:
      audio = r.listen(source)
      try:
        text = r.recognize_google(audio)
        print(text)
        if "jump" in text.lower():
          print("Action command detected!")
          keyboard.press(Key.space)
          keyboard.release(Key.space)
          break
      except sr.UnknownValueError:
        print("Could not understand audio")
      except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Defining the theme of the window
sg.theme('DarkAmber')

# Set window size
window_size = (600, 480)

# Function to list available webcam ports (replace with your system-specific logic)
def get_webcam_ports():
    webcam_ports = []
    print("Checking webcam ports ...")
    for i in range(4):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            webcam_ports.append(f"Webcam {i}")
            cap.release()
    return webcam_ports

# Get available webcam ports
webcam_ports = get_webcam_ports()

# Info window layout
info_layout = [[sg.Text("Welcome to the Inclusive Gaming Assistant!", font=('Oswald', 20, 'bold'))],
               [sg.Text("This app allows people with movement disabilities play video games. This app uses computer vision algorithms to recognise face movements and translates it into game actions.", font=('Oswald', 11))],
               [sg.Text("The app is still in development, so some of required game actions might not be available. Updates will come once in a while :) !!!", font=('Oswald', 11))],
               [sg.Text("This project has been developed for the AMD pervasive AI developer contest and has been developed by Gustavs Andersons.", font=('Oswald', 11))],
               [sg.Text("For this app to work, you have to choose your main webcam, you can do it by selecting the right port.", font=('Oswald', 11))],
               [sg.Text("Select Webcam Port:", font=('Oswald', 12, 'bold')),
                sg.Combo(webcam_ports, default_value=webcam_ports[0] if webcam_ports else None, key='webcam_port')],
               [sg.Text("Click 'Next' to proceed.", font=('Oswald', 8))],
               [sg.Button('Next', disabled=not webcam_ports, size=(20, 1), font=('Oswald', 15, 'bold'))]]  # Disable Next if no ports

# Game selection window layout (same as before)
game_layout = [
    [sg.Text("Choose a game :", font=('Oswald', 20, 'bold'))],
    [sg.Button("Tetr.io", size=(250, 1), font=('Oswald', 30, 'bold'))],
    [sg.Button("Among Us", size=(250, 1), font=('Oswald', 30, 'bold'))],
    [sg.Button("Rocket League", size=(250, 1), font=('Oswald', 30, 'bold'))],
    [sg.Push(), sg.Text("Press ESC to cancel"), sg.Push()],
]

AmongUs_layout = [
    [sg.Text("You have selected the Among Us option. This is how to control the gameplay:", font=('Oswald', 10, 'bold'))],
    [sg.Text("1) There will be a " + str(countdown_seconds) + " seccond timer that will allow you to turn on the game.", font=('Oswald', 10, 'bold'))],
    [sg.Text("2) When the tracking initilises, there will be a gentle sound.", font=('Oswald', 10, 'bold'))],
    [sg.Text("3) When it starts, you will be able to control the players position with head movements.", font=('Oswald', 10, 'bold'))],
    [sg.Text("Theres also voice commands, like action - that will either kill or report.", font=('Oswald', 10, 'bold'))],
    [sg.Text("Also, with voice control, you can stop tracking, by saying stop. You will hear a sound!", font=('Oswald', 10, 'bold'))],
    [sg.Button('Next', size=(20, 1), font=('Oswald', 15, 'bold'))]]

TetrIO_layout = [
    [sg.Text("You have selected the Tetr.io option. This is how to control the gameplay:", font=('Oswald', 10, 'bold'))],
    [sg.Text("1) There will be a " + str(countdown_seconds) + " seccond timer that will allow you to turn on the game.", font=('Oswald', 10, 'bold'))],
    [sg.Text("2) When the tracking initilises, there will be a gentle sound.", font=('Oswald', 10, 'bold'))],
    [sg.Text("3) When it starts, you will be able to control the cubes position with head movements.", font=('Oswald', 10, 'bold'))],
    [sg.Text("Theres also voice commands, like drop - that will drop the cube.", font=('Oswald', 10, 'bold'))],
    [sg.Text("Also, with voice control, you can stop tracking, by saying stop. You will hear a sound!", font=('Oswald', 10, 'bold'))],
    [sg.Button('Next', size=(20, 1), font=('Oswald', 15, 'bold'))]]

RocketL_layout = [
    [sg.Text("You have selected the Rocket League option. This is how to control the gameplay:", font=('Oswald', 10, 'bold'))],
    [sg.Text("1) There will be a " + str(countdown_seconds) + " seccond timer that will allow you to turn on the game.", font=('Oswald', 10, 'bold'))],
    [sg.Text("2) When the tracking initilises, there will be a gentle sound.", font=('Oswald', 10, 'bold'))],
    [sg.Text("3) When it starts, you will be able to control the cars heading with head movements.", font=('Oswald', 10, 'bold'))],
    [sg.Text("Theres also voice commands, like speed - that will make the car start driving, brakes - that will stop the car and boost - that will use the boost of the car and jump.", font=('Oswald', 10, 'bold'))],
    [sg.Text("Also, with voice control, you can stop tracking, by saying stop. You will hear a sound!", font=('Oswald', 10, 'bold'))],
    [sg.Button('Next', size=(20, 1), font=('Oswald', 15, 'bold'))]]

# Create the info window
info_window = sg.Window("AMD AI contest -> Inclusive Gaming", info_layout, finalize=True)

# Event loop for info window
while True:
    event, values = info_window.read()

    # Check for 'Next' button click
    if event == 'Next':
        print("Choose game")
        pygame.mixer.music.load("ClickSFX.mp3")
        pygame.mixer.music.play()
        info_window.close()  # Close the info window
        game_window = sg.Window("AMD AI contest -> Inclusive Gaming", game_layout, finalize=True, size=window_size)  # Create the game selection window
        break  # Exit the info window loop

    # Check for close button or ESC
    if event == sg.WIN_CLOSED:
        pygame.mixer.music.load("ClickSFX.mp3")
        pygame.mixer.music.play()
        break

info_window.close()

while True:
    event, values = game_window.read()

    # Check for button clicks
    if event in ("Tetr.io", "Among Us", "Rocket League"):
        print(f"You clicked: {event}")
        if event == "Tetr.io":
            pygame.mixer.music.load("ClickSFX.mp3")
            pygame.mixer.music.play()
            game_window.close()
            TetrIO_window = sg.Window("AMD AI contest -> Inclusive Gaming", TetrIO_layout, finalize=True)
            while True:
                event, values = TetrIO_window.read()

                # Check for 'Next' button click
                if event == 'Next':
                    pygame.mixer.music.load("ClickSFX.mp3")
                    pygame.mixer.music.play()
                    TetrIO_window.close()  # Close the info window
                    print("Starting recognition...")
                    engine.say("Face recognition is going to start in " + str(countdown_seconds) + " seconds. You will hear an beep.")
                    engine.runAndWait()
                    for seconds_remaining in range(countdown_seconds, 0, -1):
                        print(f"Starting in {seconds_remaining} second{'s' if seconds_remaining > 1 else ''}")
                        time.sleep(1)
                    pygame.mixer.music.load("StartSFX.aac")
                    pygame.mixer.music.play()
                    while True:
                        if __name__ == "__main__":
                            listen_for_stop()
                            listen_for_drop()

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
                            print("Left") # tetr left
                            keyboard.press(Key.left)
                            keyboard.release(Key.left)
                        if class_index == 2:
                            print("Right") # tetr right
                            keyboard.press(Key.right)
                            keyboard.release(Key.right)
                        if class_index == 3:
                            print("Up") # tetr rotate
                            keyboard.press(Key.up)
                            keyboard.release(Key.up)
                        if class_index == 4:
                            print("Down") # tetr drop
                            keyboard.press(Key.down)
                            keyboard.release(Key.down)

                        time.sleep(0.5)

                        if stop == True :
                            stop = False
                            break

                    cap.release()
                    cv2.destroyAllWindows()

                # Check for close button or ESC
                if event == sg.WIN_CLOSED:
                    pygame.mixer.music.load("ClickSFX.mp3")
                    pygame.mixer.music.play()
                    break

        if event == "Among Us":
            pygame.mixer.music.load("ClickSFX.mp3")
            pygame.mixer.music.play()
            game_window.close()
            AmongUs_window = sg.Window("AMD AI contest -> Inclusive Gaming", AmongUs_layout, finalize=True)
            while True:
                event, values = AmongUs_window.read()

                # Check for 'Next' button click
                if event == 'Next':
                    pygame.mixer.music.load("ClickSFX.mp3")
                    pygame.mixer.music.play()
                    AmongUs_window.close()  # Close the info window
                    engine.say("Face recognition is going to start in " + str(countdown_seconds) + " seconds. You will hear an beep.")
                    engine.runAndWait()
                    for seconds_remaining in range(countdown_seconds, 0, -1):
                        print(f"Starting in {seconds_remaining} second{'s' if seconds_remaining > 1 else ''}")
                        time.sleep(1)
                    print("Starting recognition...")
                    pygame.mixer.music.load("StartSFX.aac")
                    pygame.mixer.music.play()
                    while True:
                        if __name__ == "__main__":
                            listen_for_stop()
                            listen_for_action()

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
                            print("Left") # amongus
                            keyboard.press("a")
                            keyboard.release("a")
                        if class_index == 2:
                            print("Right") # amongus
                            keyboard.press("d")
                            keyboard.release("d")
                        if class_index == 3:
                            print("Up") # amongus
                            keyboard.press("w")
                            keyboard.release("w")
                        if class_index == 4:
                            print("Down") # amongus
                            keyboard.press("s")
                            keyboard.release("s")

                        time.sleep(0.5)

                        if stop == True :
                            stop = False
                            break

                    cap.release()
                    cv2.destroyAllWindows()

                # Check for close button or ESC
                if event == sg.WIN_CLOSED:
                    pygame.mixer.music.load("ClickSFX.mp3")
                    pygame.mixer.music.play()
                    break
            AmongUs_window.close()

        if event == "Rocket League":
            pygame.mixer.music.load("ClickSFX.mp3")
            pygame.mixer.music.play()
            game_window.close()
            RocketL_window = sg.Window("AMD AI contest -> Inclusive Gaming", RocketL_layout, finalize=True)
            while True:
                event, values = RocketL_window.read()

                # Check for 'Next' button click
                if event == 'Next':
                    pygame.mixer.music.load("ClickSFX.mp3")
                    pygame.mixer.music.play()
                    RocketL_window.close()  # Close the info window
                    engine.say("Face recognition is going to start in " + str(countdown_seconds) + " seconds. You will hear an beep.")
                    engine.runAndWait()
                    for seconds_remaining in range(countdown_seconds, 0, -1):
                        print(f"Starting in {seconds_remaining} second{'s' if seconds_remaining > 1 else ''}")
                        time.sleep(1)
                    print("Starting recognition...")
                    pygame.mixer.music.load("StartSFX.aac")
                    pygame.mixer.music.play()
                    while True:
                        if __name__ == "__main__":
                            listen_for_stop()
                            listen_for_speed()
                            listen_for_boost()
                            listen_for_brakes()
                            listen_for_jump()

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
                            print("Left") # RL
                            keyboard.press(Key.left)
                            keyboard.release(Key.left)
                        if class_index == 2:
                            print("Right") # RL
                            keyboard.press(Key.right)
                            keyboard.release(Key.right)

                        time.sleep(0.5)

                        if stop == True :
                            stop = False
                            break

                    cap.release()
                    cv2.destroyAllWindows()

                # Check for close button or ESC
                if event == sg.WIN_CLOSED:
                    pygame.mixer.music.load("ClickSFX.mp3")
                    pygame.mixer.music.play()
                    break

    # Check for keyboard presses
    if event == sg.WIN_CLOSED or event == 'Cancel':  # ESC key
        pygame.mixer.music.load("ClickSFX.mp3")
        pygame.mixer.music.play()
        break

game_window.close()