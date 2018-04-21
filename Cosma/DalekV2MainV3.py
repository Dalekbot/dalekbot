#!/usr/bin/env python

#======================================================================
# Place holders.  These may or may not be required

# Python 2/3 compatibility
#from __future__ import print_function

import sys
sys.settrace
#from glob import glob
#import itertools as it
import os
from operator import itemgetter
#import struct

#from imutils.object_detection import non_max_suppression
#from imutils import paths

# End of Place holders
#======================================================================


#======================================================================
# Start of Main Imports and setup constants

# Module Imports
import RPi.GPIO as GPIO  # Import GPIO divers
import time              # Import the Time library
import cwiid             # Import WiiMote code
import argparse          # Import Argument Parser
import scrollphat        # Import Scroll pHat code
import numpy as np       # Import NumPy Array manipulation
import cv2               # Import OpenCV Vision code
import DalekV2Drive      # Import my 4 Motor controller
import subprocess        # Import Modual to allow subprocess to be lunched

# Main Imports and setup constants
speed = 50               # 0 is stopped, 100 is fastest
rightspeed = 50          # 0 is stopped, 100 is fastest
leftspeed = 50           # 0 is stopped, 100 is fastest
maxspeed = 100           # Set full Power
minspeed = 0             # Set min power  
innerturnspeed = 40      # Speed for Inner Wheels in a turn
outerturnspeed = 80      # Speed for Outer Wheels in a turn
hRes = 640               # PiCam Horizontal Resolution
vRes = 480               # PiCam Virtical Resolution
camera = 0               # Create PiCamera Object
video_capture = 0        # Create WebCam Object
soundvolume = 100        # Set Default Sound Volume
TrigPinLeft = 35         # Set the Trigger pin for Left Sensor
EchoPinLeft = 37         # Set the Echo pin for Left Sensor
TrigPinCenter = 33       # Set the Trigger pin for Right Sensor
EchoPinCenter = 31       # Set the Echo pin for Center Sensor
TrigPinRight = 29        # Set the Trigger pin for Right Sensor
EchoPinRight = 32        # Set the Echo pin for Right Sensor

# End of Main Imports and setup constants
#======================================================================

#======================================================================
# Initialisation procedures

def setup():                   # Setup GPIO and Initalise Imports

    global TrigPinLeft         # Allow Access to Trigger pin for Left Sensor
    global EchoPinLeft         # Allow Access to Echo pin for Left Sensor
    global TrigPinCenter       # Allow Access to Trigger pin for Right Sensor
    global EchoPinCenter       # Allow Access to Echo pin for Center Sensor
    global TrigPinRight        # Allow Access to Trigger pin for Right Sensor
    global EchoPinRight        # Set the Echo pin for Right Sensor
    
    connected = False
    while connected == False:
        connected = setupwii() # Setup and connect to WiiMote
    GPIO.setmode(GPIO.BOARD)   # Set the GPIO pins as numbering - Also set in DalekV2Drive.py
    GPIO.setwarnings(False)    # Turn GPIO warnings off - CAN ALSO BE Set in DalekV2Drive.py

    GPIO.setup(TrigPinLeft,GPIO.OUT)   # Set the Left Trigger pin to output
    GPIO.setup(EchoPinLeft,GPIO.IN)    # Set the Left Echo pin to input
    GPIO.setup(TrigPinCenter,GPIO.OUT) # Set the Center Trigger pin to output
    GPIO.setup(EchoPinCenter,GPIO.IN)  # Set the Center Echo pin to input
    GPIO.setup(TrigPinRight,GPIO.OUT)  # Set the Right Trigger pin to output
    GPIO.setup(EchoPinRight,GPIO.IN)   # Set the Right Echo pin to input
    
    DalekV2Drive.init()        # Initialise my software to control the motors
 
    # initialize the camera and grab a reference to the raw camera capture
    global hRes                # Allow Access to PiCam Horizontal Resolution
    global vRes                # Allow Access to PiCam Vertical Resolution

    # Setup WebCam
    global video_capture        # Allow Access to WebCam Object
    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, hRes)
    video_capture.set(4, vRes)

    print ('\nPress some buttons!\n')                                     # Give instructions for connecting Wiimote
    print ('Press PLUS and MINUS together to disconnect and quit.\n')     # Give instructions for connecting Wiimote
    
#======================================================================
  
def setupwii():
    # Connect Wiimote
    print ('\nPress & hold 1 + 2 on your Wii Remote now ...\n\n')
    scrollphat.clear()         # Shutdown Scroll pHat
    scrollphat.write_string('1+2')

    # Connect to the Wii Remote. If it times out then quit.
    
    global wii

    try:
        wii=cwiid.Wiimote()
    except RuntimeError:
        print ('Error opening wiimote connection')
        scrollphat.clear()         # Shutdown Scroll pHat
        scrollphat.write_string('Err')
        time.sleep(0.5)
        return False

    print ('Wii Remote connected...\n')
    wii.rumble = 1
    time.sleep(0.1)
    wii.rumble = 0
    
    wii.led = 1
    time.sleep(0.75) 
    wii.led = 2
    time.sleep(0.75)
    wii.led = 4
    time.sleep(0.75)
    wii.led = 8
    time.sleep(0.75)
    battery = int(wii.state['battery']/25)
    
    if battery == 4:
        wii.led = 8
    elif battery == 3:
        wii.led = 4
    elif battery == 2:
        wii.led = 2
    else: 
        wii.led = 1
    
    wii.rumble = 1
    time.sleep(0.1)
    wii.rumble = 0
    
    scrollphat.clear()         # Shutdown Scroll pHat
    scrollphat.write_string('Gd')

    print ('\nPress some buttons!\n')
    print ('Press PLUS and MINUS together to disconnect and quit.\n')
    
    return True
  
# End of Initialisation procedures
#======================================================================

#======================================================================
# Service Procedures
   
def getdistance(distance, TRIG, ECHO):
    GPIO.output(TRIG, False)
    #print 'Waiting For Sensor To Settle'
    time.sleep(0.05)
    pulse_start = 0
    pulse_end = 0

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        #print 'start', GPIO.input(ECHO)
        pulse_start = time.time()
  
    while GPIO.input(ECHO)==1:
        #print 'stop', GPIO.input(ECHO)
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    #print 'Distance:',distance,'cm'
    return distance

#======================================================================
    
# ---- Function definition for converting scales ------
def remap(unscaled, to_min, to_max, from_min, from_max):
    return (to_max-to_min)*(unscaled-from_min)/(from_max-from_min)+to_min
    
def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

#======================================================================

#def draw_detections(img, rects, thickness = 1):
#    # pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
#    for x, y, w, h in rects:
#        # the HOG detector returns slightly larger rectangles than the real objects.
#        # so we slightly shrink the rectangles to get a nicer output.
#        pad_w, pad_h = int(0.15*w), int(0.05*h)
#        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)
#    # end for
#    return
    
#======================================================================
def updateServoMotorPositions(pwm, panServoPosition, tiltServoPosition):
    panDutyCycle = ((float(panServoPosition) * 0.3) + 15) * 10
    tiltDutyCycle = ((float(tiltServoPosition) * 0.1555556) + 20) * 10
    
    #pwmPanObject.ChangeDutyCycle(panDutyCycle)
    pwm.setPWM(servoHorizontalPort, 0, int(panDutyCycle))
    #pwmTiltObject.ChangeDutyCycle(tiltDutyCycle)
    pwm.setPWM(servoVerticalPort, 0, int(tiltDutyCycle))
# end function
    
# End of Service Procedures    
#======================================================================

#======================================================================
# Clean-up Procedures  
    
def destroy():                 # Shutdown GPIO and Cleanup modules

    global soundvolume         # Allow access to sound volume
        
    print ('\n... Shutting Down...\n')
    scrollphat.clear()         # Shutdown Scroll pHat
    scrollphat.write_string('Ext')
    DalekV2Drive.stop()        # Make sure Bot is not moving when program exits
    DalekV2Drive.cleanup()     # Shutdown all motor control
    global wii                 # Allow access to the wii object
    wii.rumble = 1
    time.sleep(0.5)
    wii.rumble = 0
    cv2.destroyAllWindows()    # Shutdown any open windows
    volumesetting = '"--volume=' + str(soundvolume) +'"'
    subprocess.Popen(['mplayer',volumesetting, 'Sound/Grow_stronger.mp3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(7)
    scrollphat.clear()         # Clear Scroll pHat
    GPIO.cleanup()             # Release GPIO resource
    
# End of Clean-up Procedures  
#======================================================================

#======================================================================    
# Task Procedures  

def ObstacleCourse():

    global speed               # Allow access to 'speed' constant
    global rightspeed          # Allow access to 'rightspeed' constant
    global leftspeed           # Allow access to 'leftspeed' constant
    global maxspeed            # Allow access to 'maxspeed' constant
    global minspeed            # Allow access to 'minspeed' constant
    global innerturnspeed      # Speed for Inner Wheels in a turn
    global outerturnspeed      # Speed for Outer Wheels in a turn
    global wii                 # Allow access to 'Wii' constants
    global soundvolume         # Allow access to sound volume

    wii.rpt_mode = cwiid.RPT_BTN
    
    time.sleep(2)
    
    boost = 0                                   # Turn boost off

    while True:
        buttons = wii.state['buttons']          # Get WiiMote Button Pressed
        # Choose which task to do
        
        # If Plus and Minus buttons pressed
        # together then rumble and quit.
        if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):  
           break  

        print (speed)
        scrollphat.clear()         # Shutdown Scroll pHat
        scrollphat.write_string(str(speed))
        
        if boost == 0 and (buttons & cwiid.BTN_B):
            print ('Boost', maxspeed)
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('Max')
            savespeed = speed
            speed = maxspeed
            boost = 1
            time.sleep(.25)
        elif boost == 1 and (buttons & cwiid.BTN_B):
            speed = savespeed
            boost = 0
            print ('Normal', speed)
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('Nor')
            time.sleep(.25)
        
        if (buttons & cwiid.BTN_UP):
            print ('Forward', speed)
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('Fw')
            DalekV2Drive.forward(speed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_DOWN):
            print ('Backward', speed)
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('Bw')
            DalekV2Drive.backward(speed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_LEFT):
            print ('Spin Left', speed)
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('SL')
            DalekV2Drive.spinLeft(maxspeed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_RIGHT):
            print ('Spin Right', speed)
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('SR')
            DalekV2Drive.spinRight(maxspeed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_1):
            print ('Turn Right')
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('TrR')
            DalekV2Drive.turnForwardRight(outerturnspeed, innerturnspeed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_2):
            print ('Turn Left')
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('TrL')
            DalekV2Drive.turnForwardLeft(innerturnspeed, outerturnspeed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_PLUS):
            print ('Speed Up 1')
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('+1')
            if speed < 100:
                speed = speed + 1
                time.sleep(0.5)
        elif (buttons & cwiid.BTN_MINUS):
            print ('Speed Down 1')
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('-1')
            if speed > 0:
                speed = speed - 1
                time.sleep(0.5)
        elif (buttons & cwiid.BTN_A):
            print ('Stop')
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('Stp')
            DalekV2Drive.stop()
            time.sleep(.25)
        elif (buttons & cwiid.BTN_HOME):
            DalekV2Drive.stop()
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Hm")
            print ('\n\nReturning to Main Menu\n\n')
            time.sleep(1)
            print ('Main Menu')               # Show we are on main menu
            print ('\nUp    - ObstacleCourse')
            print ('Down  - StreightLine')
            print ('Left  - MinimaMaze')
            print ('Right - Chase the Rainbow')
            print ('1     - Line Follow')
#            print ('2     - xxxxxx')
            print ('Home  - Exit\n')
            print ('Ready')
            break
    
def StreightLine():

    global speed               # Allow access to 'speed' constant
    global rightspeed          # Allow access to 'rightspeed' constant
    global leftspeed           # Allow access to 'leftspeed' constant
    global maxspeed            # Allow access to 'maxspeed' constant
    global minspeed            # Allow access to 'minspeed' constant
    global innerturnspeed      # Speed for Inner Wheels in a turn
    global outerturnspeed      # Speed for Outer Wheels in a turn
    global wii                 # Allow access to 'Wii' constants
    global soundvolume         # Allow access to sound volume
    global TrigPinLeft         # Allow Access to Trigger pin for Left Sensor
    global EchoPinLeft         # Allow Access to Echo pin for Left Sensor
    global TrigPinCenter       # Allow Access to Trigger pin for Right Sensor
    global EchoPinCenter       # Allow Access to Echo pin for Center Sensor
    global TrigPinRight        # Allow Access to Trigger pin for Right Sensor
    global EchoPinRight        # Set the Echo pin for Right Sensor
    
    leftdistance = 0           # Prime Left distance variable
    centerdistance = 0         # Prime Center distance variable
    rightdistance = 0          # Prime Right distance variable
    
    print ('\nPress "A" to start Streight Line run')
    print ('Press "Hm" to return to main menu\n')
        
    scrollphat.clear()         # Shutdown Scroll pHat
    scrollphat.write_string("'A'")
    time.sleep(.25)

    while True:
    
        buttons = wii.state['buttons']          # Get WiiMote Button Pressed

        if (buttons & cwiid.BTN_A):
            print ('Start Streight Line run')
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('SLR')
            time.sleep(.25)
            
            while True:
            
                DalekV2Drive.forward(maxspeed)
            
                buttons = wii.state['buttons']          # Get WiiMote Button Pressed
                # Choose which task to do
                if (buttons & cwiid.BTN_HOME):
                    DalekV2Drive.stop()
                    print ('\nPress "A" to start Streight Line run')
                    print ('Press "Hm" to return to main menu\n')
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string('"A"')
                    time.sleep(.25)
                    break
                # End if
                
                leftdistance = getdistance(leftdistance, TrigPinLeft, EchoPinLeft)
                centerdistance = getdistance(centerdistance, TrigPinCenter, EchoPinCenter)
                rightdistance = getdistance(rightdistance, TrigPinRight, EchoPinRight)
                
                scrollphat.write_string(str(leftdistance))
                print ('Left Distance :', leftdistance, 'Center Distance :', centerdistance, 'Right Distance :', rightdistance)
                
                if centerdistance <= 2:
                    DalekV2Drive.stop()
                    print ('\nCenter Distance :', centerdistance, 'Run Finished\n\n')
                    print ('\nPress "A" to start Streight Line run')
                    print ('Press "Hm" to return to main menu\n')
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string('"A"')
                    time.sleep(.25)
                    break
                # End if
                 
                if leftdistance <= 5:
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string('TrR')
                    DalekV2Drive.turnForwardRight(outerturnspeed, innerturnspeed)
                    time.sleep(.1)
                    DalekV2Drive.forward(maxspeed)
                # End if
                    
                if rightdistance <= 5:
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string('TrL')
                    DalekV2Drive.turnForwardLeft(innerturnspeed, outerturnspeed)
                    time.sleep(.1)
                    DalekV2Drive.forward(maxspeed)
                # End if

            # End While
                
        elif (buttons & cwiid.BTN_HOME):
            DalekV2Drive.stop()
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Hm")
            print ('\n\nReturning to Main Menu\n\n')
            time.sleep(1)
            print ('Main Menu')               # Show we are on main menu
            print ('\nUp    - ObstacleCourse')
            print ('Down  - StreightLine')
            print ('Left  - MinimaMaze')
            print ('Right - Chase the Rainbow')
            print ('1     - Line Follow')
#            print ('2     - xxxxxx')
            print ('Home  - Exit\n')
            print ('Ready')
            break
        # End if
    
#def MinimuMaze():

def LineFollow(showcam):

    global speed               # Allow access to 'speed' constant
    global rightspeed          # Allow access to 'rightspeed' constant
    global leftspeed           # Allow access to 'leftspeed' constant
    global maxspeed            # Allow access to 'maxspeed' constant
    global minspeed            # Allow access to 'minspeed' constant
    global innerturnspeed      # Speed for Inner Wheels in a turn
    global outerturnspeed      # Speed for Outer Wheels in a turn
    global wii                 # Allow access to 'Wii' constants
    global hRes                # Allow Access to Cam Horizontal Resolution
    global vRes                # Allow Access to Cam Vertical Resolution
    global video_capture       # Allow Access to WebCam Object
    global soundvolume         # Allow access to sound volume
    
    cx = 300                   # Go Streight
    turnspeed = 95
    speed = 30
    
    print ('\nPress "A" to start Line following')
    print ('Press "Hm" to return to main menu\n')
        
    scrollphat.clear()         # Shutdown Scroll pHat
    scrollphat.write_string('"A"')
    time.sleep(.25)

    while True:
    
        buttons = wii.state['buttons']          # Get WiiMote Button Pressed

        if (buttons & cwiid.BTN_A):
            print ('Start Line Following')
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('LiF')
            time.sleep(.25)
            cx = 300                   # Go Streight
            
            while True:
            
                buttons = wii.state['buttons']          # Get WiiMote Button Pressed
                # Choose which task to do
                if (buttons & cwiid.BTN_HOME):
                    DalekV2Drive.stop()
                    print ('\nPress "A" to start Line following')
                    print ('Press "Hm" to return to main menu\n')
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string('"A"')
                    time.sleep(.25)
                    break
            
                # Capture from camera
                ret, frame = video_capture.read()
     
                # Crop, select part of image to work with
                crop_img = frame[380:480, 0:640]

                # Make the image greyscale
                gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

                # uncomment next line to view greyscale image
                #cv2.imshow('Gray',gray) 
 
                # Apply a Gaussian blur
                blur = cv2.GaussianBlur(gray,(5,5),0)

                # uncomment next line to view Blurred image
                #cv2.imshow('Blur',blur)
 
                # Apply Color thresholding
                ret,thresh = cv2.threshold(blur,100,255,cv2.THRESH_BINARY_INV)

                # uncomment next line to view Threshholded image    
                #cv2.imshow('Thresh',thresh)
 
                # Find the contours in the cropped image part
                img, contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

                # ---------------- Find the biggest contour = line -----------------
    
                if len(contours) > 0:
                    c = max(contours, key=cv2.contourArea)
                    M = cv2.moments(c)
 
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
 
                    cv2.line(crop_img,(cx,0),(cx,720),(255,255,0),2)
                    cv2.line(crop_img,(0,cy),(1280,cy),(0,255,0),2)
                    cv2.drawContours(crop_img, contours, -1, (0,255,255), 2)

                    # ---- Draw centre boundry lines (Steer straight)
                    cv2.line(crop_img,(270,0),(270,480),(0,0,255),2)
                    cv2.line(crop_img,(370,0),(370,480),(0,0,255),2)

                # --------- Steer Right Routine ----------
                if cx >= 370:
                    RSteer = cx - 370
                    SteerRight = remap(RSteer, 0, 45, 1, 270)
                    print ('Turn Right: ', SteerRight, cx)
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string('TrR')
                    DalekV2Drive.spinRight(turnspeed)

                # --------- On Track Routine ----------
                if cx < 370 and cx > 270:
                    print ('On Track', cx)
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string('Fw')
                    DalekV2Drive.forward(speed)

                # --------- Steer Left Routine ----------
                if cx <= 270:
                    LSteer = 270 - cx
                    SteerLeft = remap(LSteer, 0, 45, 1, 270)
                    print ('Turn Left: ', SteerLeft, cx)
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string('TrL')
                    DalekV2Drive.spinLeft(turnspeed)
 
                # ------ Show the resulting cropped image
                if showcam == True:
                    cv2.imshow('frame',crop_img)
                # ------ Exit if Q pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                                
        elif (buttons & cwiid.BTN_HOME):
            DalekV2Drive.stop()
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Hm")
            print ('\n\nReturning to Main Menu\n\n')
            time.sleep(1)
            print ('Main Menu')               # Show we are on main menu
            print ('\nUp    - ObstacleCourse')
            print ('Down  - StreightLine')
            print ('Left  - MinimaMaze')
            print ('Right - Chase the Rainbow')
            print ('1     - Line Follow')
#            print ('2     - xxxxxx')
            print ('Home  - Exit\n')
            print ('Ready')
            break
            
def Rainbow(showcam):

    global speed               # Allow access to 'speed' constant
    global rightspeed          # Allow access to 'rightspeed' constant
    global leftspeed           # Allow access to 'leftspeed' constant
    global maxspeed            # Allow access to 'maxspeed' constant
    global minspeed            # Allow access to 'minspeed' constant
    global innerturnspeed      # Speed for Inner Wheels in a turn
    global outerturnspeed      # Speed for Outer Wheels in a turn
    global wii                 # Allow access to 'Wii' constants
    global hRes                # Allow Access to Cam Horizontal Resolution
    global vRes                # Allow Access to Cam Vertical Resolution
    global video_capture       # Allow Access to WebCam Object
    global soundvolume         # Allow access to sound volume

    turnspeed = 95
    
    print ('Checkpoint: Set up WebCam\n')
	# initialize the camera and grab a reference to the raw camera capture
    
    hRes = 320
    vRes = 240
    
    print ('default resolution = ' + str(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)) + 'x' + str(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, hRes)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, vRes)

    print ('updated resolution = ' + str(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)) + 'x' + str(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

#    if video_capture.isOpened() == False:                           # check if VideoCapture object was associated to webcam successfully
#        print 'error: video_capture not accessed successfully\n\n'  # if not, print error message to std out
#        os.system('pause')                                          # pause until user presses a key so user can see error message
#        wait = input('PRESS ENTER TO CONTINUE.\n\n')
#        return                                                      # and exit function (which exits program)
#    # end if

    intXFrameCenter = int(float(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)) / 2.0)
    intYFrameCenter = int(float(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) / 2.0)
   
    #print intXFrameCenter, intYFrameCenter
    
    if intXFrameCenter == 0.0:
        scrollphat.clear()         # Shutdown Scroll pHat
        scrollphat.write_string('Err')
        time.sleep(2)
        return
    
    panServoPosition = intXFrameCenter
    
    print ('\nPress "A" to Chase the Rainbow')
    print ('Press "Hm" to return to main menu\n')
        
    scrollphat.clear()         # Shutdown Scroll pHat
    scrollphat.write_string('"A"')
    time.sleep(.25)

    #print 'Checkpoint: Enter main Loop\n\n'
   
    while True:
    
        buttons = wii.state['buttons']          # Get WiiMote Button Pressed
        
        if (buttons & cwiid.BTN_A):
            print ('Start Chasing the Rainbow')
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('CtR')
            time.sleep(.25)
 
            while True:
            
                buttons = wii.state['buttons']          # Get WiiMote Button Pressed
                
                if (buttons & cwiid.BTN_HOME):
                    DalekV2Drive.stop()
                    print ('\nPress "A" to Chase the Rainbow 1 ')
                    print ('Press "Hm" to return to main menu\n')
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string('"A"')
                    time.sleep(.25)
                    break

                while video_capture.isOpened():                    # cv2.waitKey(1) != 32 and until the Esc key is pressed or webcam connection is lost
                    blnFrameReadSuccessfully, imgOriginal = video_capture.read()            # read next frame

                    buttons = wii.state['buttons']          # Get WiiMote Button Pressed
                    
                    if (buttons & cwiid.BTN_HOME):
                        DalekV2Drive.stop()
                        print ('\nPress "A" to Chase the Rainbow 2')
                        print ('Press "Hm" to return to main menu\n')
                        scrollphat.clear()         # Shutdown Scroll pHat
                        scrollphat.write_string('"A"')
                        time.sleep(.25)
                        break
                    # end if
                    
                    if not blnFrameReadSuccessfully or imgOriginal is None:             # if frame was not read successfully
                        print ('error: frame not read from webcam\n')                     # print error message to std out
                        #os.system('pause')                                             # pause until user presses a key so user can see error message
                        break                                                           # exit while loop (which exits program)
                    # end if

                    #print ('Checkpoint: Picture Taken - Starting Analysis')
		
                    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)
                    
                    imgThreshLow = cv2.inRange(imgHSV, np.array([0, 135, 135]), np.array([19, 255, 255]))
                    imgThreshHigh = cv2.inRange(imgHSV, np.array([168, 135, 135]), np.array([179, 255, 255]))
                    
                    imgThresh = cv2.add(imgThreshLow, imgThreshHigh)
                    
                    imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)

                    imgThresh = cv2.dilate(imgThresh, np.ones((5,5),np.uint8))
                    imgThresh = cv2.erode(imgThresh, np.ones((5,5),np.uint8))

                    intRows, intColumns = imgThresh.shape

                    #print ('Checkpoint : 2')
                    
                    circles = cv2.HoughCircles(imgThresh, cv2.HOUGH_GRADIENT, 3, intRows / 4)      # fill variable circles with all circles in the processed image

                    if circles is not None:                     # this line is necessary to keep program from crashing on next line if no circles were found
                
                        sortedCircles = sorted(circles[0], key = itemgetter(2), reverse = True)

                        largestCircle = sortedCircles[0]

                        x, y, radius = largestCircle                                                                       # break out x, y, and radius
                        print ('ball position x = ' + str(x) + ', y = ' + str(y) + ', radius = ' + str(radius))       # print ball position and radius
			
                        scrollphat.clear()
                        scrollphat.write_string('Red')
                        DalekV2Drive.forward(speed)

                        if x < intXFrameCenter and panServoPosition >= 2:
                            panServoPosition = panServoPosition - 2
                            print ('Turn Left: ', panServoPosition)
                            scrollphat.clear()         # Shutdown Scroll pHat
                            scrollphat.write_string('TrL')
                            DalekV2Drive.spinLeft(turnspeed)
                            time.sleep(.25)
                            DalekV2Drive.stop()
                        elif x > intXFrameCenter and panServoPosition <= 178:
                            panServoPosition = panServoPosition + 2
                            print ('Turn Right: ', panServoPosition)
                            scrollphat.clear()         # Shutdown Scroll pHat
                            scrollphat.write_string('TrR')
                            DalekV2Drive.spinRight(turnspeed)
                            time.sleep(.25)
                            DalekV2Drive.stop()
                        # end if else
                        
                        if showcam == True:
                                cv2.circle(imgOriginal, (x, y), 3, (0, 255, 0), -1)           # draw small green circle at center of detected object
                                cv2.circle(imgOriginal, (x, y), radius, (0, 0, 255), 3)       # draw red circle around the detected object
                                cv2.imshow('imgOriginal', imgOriginal)                        # show windows
                                cv2.imshow('imgThresh', imgThresh)
                        # end if
                    else:
                        panServoPosition = panServoPosition - 2
                        print ('Turn Right: ', panServoPosition)
                        scrollphat.clear()         # Shutdown Scroll pHat
                        scrollphat.write_string('TrR')
                        DalekV2Drive.spinRight(turnspeed)
                        time.sleep(.25)
                        DalekV2Drive.stop()
                        if showcam == True:
                            cv2.imshow('imgOriginal', imgOriginal)                        # show windows
                            cv2.imshow('imgThresh', imgThresh)
                        # end if
                    # end if
                    
#                    	if showcam == True:
#                        	cv2.imshow('imgOriginal', imgOriginal)                        # show windows
#                        	cv2.imshow('imgThresh', imgThresh)
#                     	end if
                    
                # end while 
            # end while
            #cv2.destroyAllWindows()

    
        elif (buttons & cwiid.BTN_HOME):
            DalekV2Drive.stop()
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Hm")
            print ('\n\nReturning to Main Menu\n\n')
            time.sleep(1)
            print ('Main Menu')               # Show we are on main menu
            print ('\nUp    - ObstacleCourse')
            print ('Down  - StreightLine')
            print ('Left  - MinimaMaze')
            print ('Right - Chase the Rainbow')
            print ('1     - Line Follow')
#            print ('2     - xxxxxx')
            print ('Home  - Exit\n')
            print ('Ready')
            break
            
# End of Task Procedures  
#======================================================================    

#======================================================================    
# Main Control Procedure
    
def maincontrol(showcam):                  # Main Control Loop

    global wii                      # Allow access to 'Wii' constants
    global soundvolume              # Allow access to sound volume

    scrollphat.clear()              # Clear Scroll pHat
    scrollphat.write_string('Mn')   # Show we are on main menu
    print ('Main Menu')               # Show we are on main menu

    print ('\nUp    - ObstacleCourse')
    print ('Down  - StreightLine')
    print ('Left  - MinimaMaze')
    print ('Right - Chase the Rainbow')
    print ('1     - Line Follow')
#    print ('2     - xxxxxx')
    print ('Home  - Exit\n')
    
    wii.rpt_mode = cwiid.RPT_BTN

    print ('Ready')
    
    while True:
    
        scrollphat.clear()              # Clear Scroll pHat
        scrollphat.write_string('Mn')   # Show we are on main menu

        buttons = wii.state['buttons']          # Get WiiMote Button Pressed
        # Choose which task to do
     
        # If Plus and Minus buttons pressed
        # together then rumble and quit.
        if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):  
            break  
 
        if (buttons & cwiid.BTN_UP):
            print ('ObstacleCourse')
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string('OC')
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(['mplayer',volumesetting, 'Sound/Rant.mp3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ObstacleCourse()
        elif (buttons & cwiid.BTN_DOWN):
            print ('StreightLine')
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string('StL')
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(['mplayer',volumesetting, 'Sound/Stay.mp3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)
            StreightLine()
        elif (buttons & cwiid.BTN_LEFT):
            print ('MinimalMaze')
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string('MM')
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(['mplayer',volumesetting, 'Sound/IntruderLocated.mp3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)
            #MinimalMaze()
        elif (buttons & cwiid.BTN_RIGHT):
            print ('Chase the Rainbow')
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string('CtR')
            time.sleep(1)
            Rainbow(showcam)
        elif (buttons & cwiid.BTN_1):
            print ('Line Follow')
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string('LiF')
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(['mplayer',volumesetting, 'Sound/IntruderLocated.mp3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            LineFollow(showcam)
#        elif (buttons & cwiid.BTN_2):
#            print ('xxxxxx')
#            scrollphat.clear()         # Clear Scroll pHat
#            scrollphat.write_string('LiF')
#            LineFollowPiCam(showcam)
        elif (buttons & cwiid.BTN_PLUS):
            print ('+')
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string('+')
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(['mplayer',volumesetting, 'Sound/exterminate.mp3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif (buttons & cwiid.BTN_MINUS):
            print ('-')
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string('-')
        elif (buttons & cwiid.BTN_HOME): #or (buttons & cwiid.BTN_A):
            break

        DalekV2Drive.stop()

# End of Main Control Procedure        
#======================================================================            

#======================================================================            
# __Main__ Startup Loop        
       
if __name__ == '__main__': # The Program will start from here
        
    # Get and parse Arguments
    parser = argparse.ArgumentParser(description='PiWars Dalek Control Program')
    parser.add_argument('-r',dest='RightSpeed', type=float, help='Initial speed of Right motors (0 - 100)')       # Initial speed of Right Motors
    parser.add_argument('-l',dest='LeftSpeed', type=float, help='Initial speed of Left Motors (0 - 100)')         # Initial speed of Left Motors
    parser.add_argument('-s',dest='Speed', type=float, help='Initial General speed of Motors (0 - 100)')          # Initial General speed of Motors
    parser.add_argument('-b',dest='Brightness', type=float, help='Brightness of scrollpHat (0 - 5)')              # Brightness of scrollpHat
    parser.add_argument('-i',dest='InnerTurnSpeed', type=float, help='Speed of Inner wheels in a turn (0 - 100)') # Speed of Inner wheels in a turn
    parser.add_argument('-o',dest='OuterTurnSpeed', type=float, help='Speed of Inner wheels in a turn (0 - 100)') # Speed of Outer wheels in a turn
    parser.add_argument('-c',dest='ShowCam', type=bool, help='Show Image from Active Cam (True/False)')           # Show Image from Active Cam
    parser.add_argument('-v',dest='SoundVolume', type=int, help='Set Sound volume (0 - 100)')                     # Set Sound Volume
    args = parser.parse_args()
    
    if ((str(args.RightSpeed)) != 'None'):
        print ('\nRight Speed - ',(str(args.RightSpeed)))
        rightspeed = args.RightSpeed

    if ((str(args.LeftSpeed)) != 'None'):
        print ('Left Speed - ',(str(args.LeftSpeed)))
        leftspeed = args.LeftSpeed

    if ((str(args.Speed)) != 'None'):
        print ('\nGeneral Speed - ',(str(args.Speed)))
        speed = args.Speed
    
    if ((str(args.Brightness)) != 'None'):
        print ('\nscrollpHat Brightness - ',(str(args.Brightness)))
        scrollphat.set_brightness(int(args.Brightness))

    if ((str(args.InnerTurnSpeed)) != 'None'):
        print ('\nInner Turn Speed - ',(str(args.InnerTurnSpeed)))
        innerturnspeed = args.InnerTurnSpeed
    
    if ((str(args.OuterTurnSpeed)) != 'None'):
        print ('\nOuter Turn Speed - ',(str(args.OuterTurnSpeed)))
        outerturnspeed = args.OuterTurnSpeed
 
    if ((str(args.ShowCam)) != 'None'):
        print ('\nShow Cam Image - ',(str(args.ShowCam)))
        showcam = args.ShowCam
    else:
        showcam = False

    if ((str(args.SoundVolume)) != 'None'):
        print ('\nSound Volume - ',(str(args.SoundVolume)))
        soundvolume = args.SoundVolume
    else:
        soundvolume = 100
        
    print ('\n\nSetting Up ...\n')
    scrollphat.clear()         # Clear Scroll pHat
    scrollphat.write_string('Set')
    
    volumesetting = '"--volume=' + str(soundvolume) +'"'
    subprocess.Popen(['mplayer',volumesetting, 'Sound/Beginning.mp3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    setup()           # Setup all motors and Wii

    print ('\nGo ...\n\n')
    scrollphat.clear()         # Clear Scroll pHat
    scrollphat.write_string('Go')
	
    try:
        maincontrol(showcam)    # Call main loop
        destroy()     # Shutdown
        print ('\n\n................... Exit .......................\n\n')
        exit(0) # Exit Cleanly
    except KeyboardInterrupt:
        destroy()
        print ('\n\n................... Exit .......................\n\n')
        exit(0) # Exit Cleanly
        
# End of __Main__ Startup Loop 
#======================================================================

