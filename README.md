# A Bot developed for the seminar Praktikum Mechatronik
This is the code run by the bot built by a couple of colleagues and me during Praktikum Mechatronik

Bot and Software built by:
- Christoferis
- Hikaruhoshi1
- PassionNcs

## Repository includes:
- Bot Code (pm_bot)
    - Code handling Data Communication
    - Servo Controlling Code

- Host Side Code (pm_app)
    - Visualization
    - Code handling Data Communication
    - Code handling Connection to Bot

## Credits
This repository features code, libraries and ideas from other people and projects:
- Gamepad Library (& Visualization) (Python; provided by the Faculty)
- ProtocolStackV2 (Idea, C Implementation; Developed during Softwareprojekt für Ingenieure by linuxuserjtb, christoferis, hikaruhoshi1, exitium, blacky_01)
- Libraries for the Parallax Propeller ActivityBoard

## Building
To build this project following things are needed:
- Python 3.13
- SimpleIDE by Parallax or propgcc

As the provided Joystick API uses Microsoft DirectInput, the Python Code is only runnable on Windows