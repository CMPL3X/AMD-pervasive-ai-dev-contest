import time
import PySimpleGUI as sg
import cv2  # Import OpenCV for webcam testing (optional)
from pydub import AudioSegment
from pydub.playback import play  # For audio notif

# Defining the theme of the window
sg.theme('DarkAmber')

# Set window size
window_size = (600, 480)

# Audio notification for button press
Click = AudioSegment.from_file("ClickSFX.mp3", format="mp3")

# Function to list available webcam ports (replace with your system-specific logic)
def get_webcam_ports():
    webcam_ports = []
    for i in range(10):  # Check for up to 10 webcams (adjust as needed)
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
    [sg.Text("1) There will be a 15 seccond timer that will allow you to turn on the game.", font=('Oswald', 10, 'bold'))],
    [sg.Text("2) When the tracking initilises, there will be a gentle sound.", font=('Oswald', 10, 'bold'))],
    [sg.Text("3) When it starts, you will be able to control the players position with head movements.", font=('Oswald', 10, 'bold'))],
    [sg.Text("Theres also voice commands, like action - that will either kill or report.", font=('Oswald', 10, 'bold'))],
    [sg.Text("Also, with voice control, you can stop or pause tracking, by saying stop or pause. You will hear a sound!", font=('Oswald', 10, 'bold'))],
    [sg.Button('Next', size=(20, 1), font=('Oswald', 15, 'bold'))]]

# Create the info window
info_window = sg.Window("AMD AI contest -> Inclusive Gaming", info_layout, finalize=True)

# Event loop for info window
while True:
    event, values = info_window.read()

    # Check for 'Next' button click
    if event == 'Next':
        info_window.close()  # Close the info window
        play(Click)
        game_window = sg.Window("AMD AI contest -> Inclusive Gaming", game_layout, finalize=True, size=window_size)  # Create the game selection window
        break  # Exit the info window loop

    # Check for close button or ESC
    if event == sg.WIN_CLOSED:
        play(Click)
        break

info_window.close()

while True:
    event, values = game_window.read()

    # Check for button clicks
    if event in ("Tetr.io", "Among Us", "Rocket League"):
        print(f"You clicked: {event}")  # You can add custom actions for each button here
        if event == "Tetr.io":
            game_window.close()
            play(Click)
        if event == "Among Us":
            game_window.close()
            play(Click)
            AmongUs_window = sg.Window("AMD AI contest -> Inclusive Gaming", AmongUs_layout, finalize=True)
            while True:
                event, values = AmongUs_window.read()

                # Check for 'Next' button click
                if event == 'Next':
                    AmongUs_window.close()  # Close the info window
                    play(Click)
                    time.sleep(15);
                    print("Starting recognition...")
                    break

                # Check for close button or ESC
                if event == sg.WIN_CLOSED:
                    play(Click)
                    break

            AmongUs_window.close()
        if event == "Rocket League":
            game_window.close()
            play(Click)

    # Check for keyboard presses
    if event == sg.WIN_CLOSED or event == 'Cancel':  # ESC key
        break
    play(Click)

game_window.close()