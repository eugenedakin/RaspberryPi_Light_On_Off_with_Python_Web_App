# RaspberryPi_Light_On_Off_with_Python_Web_App
Turns a local light on/off using a Flask Python3 server, and a QR code to activate the web app

This python3 code is a web application where you can type/scan a QR code to the web server/app and press a button to turn on/off a light. I use this for demonstration purposes. This was created on 20 Mar 2026. Below is a short video showing the on/off button and implementation.

![](https://github.com/eugenedakin/RaspberryPi_Light_On_Off_with_Python_Web_App/blob/main/Python3LightOnOffRev3.gif)

Installation instructions:
1. Create a folder on the desktop of the Raspberry Pi (Mine is /home/dakserver/Desktop/New/FlaskLED)
2. In the FlaskLED directory, type: python3 -m venv venv //this creates a virtual machine
3. Start the virtual machine: source ./venv/bin/activate
4. Install Flask (web application program): pip3 install flask RPi.GPIO
5. Start python3 web app: python3 ledtoggleRev2.py

Below is a screen grab of the web app running on a Pixel 9:
![](https://github.com/eugenedakin/RaspberryPi_Light_On_Off_with_Python_Web_App/blob/main/ScreenshotPixel9.png)
