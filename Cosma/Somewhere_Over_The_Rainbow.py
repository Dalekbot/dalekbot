#!/usr/bin/env python

#======================================================================
# Place holders.  These may or may not be required

# Python 2/3 compatibility
from __future__ import print_function

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
from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
from dalek import spi            # Import the Spi Raspi to Arduino libray

#from dalek import controller     # Import the PS3 controller


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
    global rawCapture
    #video_capture = cv2.VideoCapture(0)
    video_capture = picamera.PiCamera()

    hRes = 320
    vRes = 240

    #video_capture.set(3, hRes)
    #video_capture.set(4, vRes)

    #camera.resolution = (hRes,vRes)
    print ("default resolution = " + str(video_capture.resolution))
    video_capture.resolution = (hRes,vRes)
    print ("updated resolution = " + str(video_capture.resolution))
    video_capture.framerate = 32
    video_capture.hflip = True
    rawCapture = PiRGBArray(video_capture, size=(hRes, vRes))

    spi.init()                 # Initialise my software for the MOSI/spi Bus

    # allow the camera to warmup
    time.sleep(0.1)

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
    global video_capture       # Allow Access to WebCam Object
    global rawCapture          # Allow Access to Raw image Capture
 

    turnspeed = 95
    dalekData = spi.readDevice1Data()
    
    print ('Checkpoint: Set up WebCam\n')

    if video_capture._check_camera_open() == False:                           # check if VideoCapture object was associated to webcam successfully
        print ("error: capWebcam not accessed successfully\n\n")          # if not, print error message to std out
        os.system("pause")                                              # pause until user presses a key so user can see error message
        return                                                          # and exit function (which exits program)
    # end if

    intXFrameCenter = int(float(hRes) / 2.0)
    intYFrameCenter = int(float(vRes) / 2.0)
   
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

            colours = ['Red', 'Blue', 'Yellow', 'Green']

            for colour in range(len(colours)): 
            
                print(colour)
                
                if colour == 0:
                    imHigh1 = [0, 135, 135]
                    imHigh2 = [19, 255, 255]
                    imLow1 = [168, 135, 135]
                    imLow2 = [179, 255, 255]
                elif colour == 1:
                    imHigh1 = [30,100,50]
                    imHigh2 = [30,100,50]
                    imLow1 = [80,250,255]
                    imLow2 = [80,250,255]
                elif colour == 2:
                    imHigh1 = [30,100,50]
                    imHigh2 = [30,100,50]
                    imLow1 = [80,250,255]
                    imLow2 = [80,250,255]
                elif colour == 3:
                    imHigh1 = [30,100,50]
                    imHigh2 = [30,100,50]
                    imLow1 = [80,250,255]
                    imLow2 = [80,250,255]
                #EndIf


                while dalekData >= 10:
            
                    buttons = wii.state['buttons']          # Get WiiMote Button Pressed
                
                    if (buttons & cwiid.BTN_HOME):
                        DalekV2Drive.stop()
                        print ('\nPress "A" to Chase the Rainbow 1 ')
                        print ('Press "Hm" to return to main menu\n')
                        scrollphat.clear()         # Shutdown Scroll pHat
                        scrollphat.write_string('"A"')
                        time.sleep(.25)
                        break

#                while video_capture.isOpened():                    # cv2.waitKey(1) != 32 and until the Esc key is pressed or webcam connection is lost
#                    blnFrameReadSuccessfully, imgOriginal = video_capture.read()            # read next frame

                    while video_capture._check_camera_open() != False:                 # cv2.waitKey(1) != 27 and 
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
                    
                        # capture frames from the camera
                        for frame in video_capture.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                            # grab the raw NumPy array representing the image, then initialize the timestamp
                            # and occupied/unoccupied text
                            imgOriginal = frame.array

                            # clear the stream in preparation for the next frame
                            rawCapture.truncate(0)
                        
                            break           # read next frame


                        #print ('Checkpoint: Picture Taken - Starting Analysis')
		
                        imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)
                    
                        #imgThreshLow = cv2.inRange(imgHSV, np.array([0, 135, 135]), np.array([19, 255, 255]))
                        #imgThreshHigh = cv2.inRange(imgHSV, np.array([168, 135, 135]), np.array([179, 255, 255]))
                    
                        imgThreshLow = cv2.inRange(imgHSV, np.array(imHigh1), np.array(imHigh2))
                        imgThreshHigh = cv2.inRange(imgHSV, np.array(imLow1), np.array(imLow2))
                    
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

                            if x > (intXFrameCenter - 9) and x > (intXFrameCenter + 9):
                                #panServoPosition = panServoPosition - 2
                                print ('Streight: ', panServoPosition)
                                scrollphat.clear()         # Shutdown Scroll pHat
                                scrollphat.write_string('Str')
                                DalekV2Drive.Forward(speed)
                                time.sleep(.25)
                                DalekV2Drive.stop()
                            elif x < (intXFrameCenter - 10) and panServoPosition >= 2:
                                panServoPosition = panServoPosition - 2
                                print ('Turn Left: ', panServoPosition)
                                scrollphat.clear()         # Shutdown Scroll pHat
                                scrollphat.write_string('TrL')
                                DalekV2Drive.spinLeft(turnspeed)
                                time.sleep(.25)
                                DalekV2Drive.stop()
                            elif x > (intXFrameCenter + 10) and panServoPosition <= 178:
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
                    
            	    #if showcam == True:
                    # 	cv2.imshow('imgOriginal', imgOriginal)                        # show windows
                    #   	cv2.imshow('imgThresh', imgThresh)
                        # 	end if
                    
                    # end while 
                aaaaaaaaaaaaaaaaaaaaaaa
                # end while
                #cv2.destroyAllWindows()

    
        elif (buttons & cwiid.BTN_HOME):
            DalekV2Drive.stop()
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Hm")
            print ('\n\nReturning to Main Menu\n\n')
            time.sleep(1)
            print ('Main Menu')               # Show we are on main menu
            print ('Right - Chase the Rainbow')
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

    print ('Right - Chase the Rainbow')
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
 
        if (buttons & cwiid.BTN_RIGHT):
            print ('Chase the Rainbow')
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string('CtR')
            time.sleep(1)
            Rainbow(showcam)
        
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

