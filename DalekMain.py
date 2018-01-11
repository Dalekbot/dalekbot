#!/usr/bin/env python

#style guide https://google.github.io/styleguide/pyguide.html

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
#import cwiid             # Import WiiMote code
import argparse          # Import Argument Parser
# import scrollphat        # Import Scroll pHat code
import numpy as np       # Import NumPy Array manipulation
import cv2               # Import OpenCV Vision code
import subprocess        # Import Modual to allow subprocess to be lunched
import DalekV2Drive      # Import my 4 Motor controller
from   DalekDebug import DalekPrint, DalekDebugOn , DalekDebugSetOutputDevice, DalekDebugSetBrightness, DalekDebugClear,DalekDebugDestroy
import DalekSpi
import joystick          # Inport the PS3 controller

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

currentChallenge = 1       # set the current Challenge we have selected


# End of Main Imports and setup constants
#======================================================================

#======================================================================
# Initialisation procedures

def setup():                   # Setup GPIO and Initalise Imports
    
    DalekDebugOn()             # use the debug and turn on output 
    DalekDebugSetOutputDevice("scrollphat") # if left empty then default is just stout

    GPIO.setmode(GPIO.BOARD)   # Set the GPIO pins as numbering - Also set in DalekV2Drive.py
    GPIO.setwarnings(False)    # Turn GPIO warnings off - CAN ALSO BE Set in DalekV2Drive.py

    DalekV2Drive.init()        # Initialise the software to control the motors
    DalekSpi.init()            # Initialise my software for the MOSI/spi Bus
    joystick.init()            # Initialise the Joystick software
  
    # this should not be needed as we are only using the value not rebinding a new value to it. 
    # initialize the camera and grab a reference to the raw camera capture
    global hRes                # Allow Access to PiCam Horizontal Resolution
    global vRes                # Allow Access to PiCam Vertical Resolution

    # Setup WebCam
    global video_capture        # Allow Access to WebCam Object
    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, hRes)
    video_capture.set(4, vRes)
    
    
  
# End of Initialisation procedures
#======================================================================
# Service Procedures
   

    
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
        
    DalekPrint( "\n... Shutting Down...\n" ,"Ext")
    
    DalekV2Drive.stop()        # Make sure Bot is not moving when program exits
    DalekV2Drive.cleanup()     # Shutdown all motor control
    time.sleep(0.5)
    cv2.destroyAllWindows()    # Shutdown any open windows
    volumesetting = '"--volume=' + str(soundvolume) +'"'
    subprocess.Popen(["mplayer",volumesetting, "Sound/Grow_stronger.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(7)
    DalekDebugDestroy()        # Clear Scroll pHat
    GPIO.cleanup()             # Release GPIO resource
    
# End of Clean-up Procedures  
#======================================================================

#======================================================================    
# Task Procedures  

# challenge_ObstacleCourse.py
# challenge_StraightLine.py:
# challenge_MinimalMaze.py:
# challenge_LineFollow.py
# challenge_OverTheRainbow.py

#======================================================================    
# Main Control Procedure
    
def maincontrol(showcam):                  # Main Control Loop

    global currentChallenge
    global soundvolume              # Allow access to sound volume
    global speed
    
    settings = {'speed': speed,
                 'currentChallenge':currentChallenge,
                 'soundVolume':soundvolume}
    
    joystick.use(settings)


   

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
        # print '\nRight Speed - ',(str())
        DalekPrint("\nRight Speed - {}".format(args.RightSpeed))
        rightspeed = args.RightSpeed

    if ((str(args.LeftSpeed)) != 'None'):
        # print 'Left Speed - ',(str(args.LeftSpeed))
        DalekPrint("\nLeft Speed - {}".format(args.LeftSpeed))
        leftspeed = args.LeftSpeed

    if ((str(args.Speed)) != 'None'):
        # print '\nGeneral Speed - ',(str(args.Speed))
        DalekPrint("\nGeneral Speed - {}".format(args.Speed))
        speed = args.Speed
    
    if ((str(args.Brightness)) != 'None'):
        # DalekPrint( '\nscrollpHat Brightness - ',(str(args.Brightness))
        DalekPrint("\nscrollpHat Brightness - {}".format(args.Brightness))
        DalekDebugSetBrightness(int(args.Brightness))

    if ((str(args.InnerTurnSpeed)) != 'None'):
        # print '\nInner Turn Speed - ',(str(args.InnerTurnSpeed))
        DalekPrint("\nInner Turn Speed - {}".format(args.InnerTurnSpeed))
        innerturnspeed = args.InnerTurnSpeed
    
    if ((str(args.OuterTurnSpeed)) != 'None'):
        # print '\nOuter Turn Speed - ',(str(args.OuterTurnSpeed))
        DalekPrint("\nOuter Turn Speed - {}".format(args.OuterTurnSpeed))
        outerturnspeed = args.OuterTurnSpeed
 
    if ((str(args.ShowCam)) != 'None'):
        # print '\nShow Cam Image - ',(str(args.ShowCam))
        DalekPrint("\nShow Cam Image - {}".format(args.ShowCam))
        showcam = args.ShowCam
    else:
        showcam = False

    if ((str(args.SoundVolume)) != 'None'):
        # print '\nSound Volume - ',(str(args.SoundVolume))
        DalekPrint("\nSound Volume - {}".format(args.SoundVolume))
        soundvolume = args.SoundVolume
    else:
        soundvolume = 100
    
    DalekPrint("\n\nSetting Up ...","Set")
    
    
    volumesetting = '"--volume=' + str(soundvolume) +'"'
    subprocess.Popen(["mplayer",volumesetting, "Sound/Beginning.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    setup()           # Setup all motors 
    DalekPrint("\nGo ...\n\n","Go")
    
	
    try:
        DalekPrint("OK 1")
        maincontrol(showcam)    # Call main loop
        DalekPrint("OK 2")

        destroy()     # Shutdown
        DalekPrint( "\n\n................... Exit .......................\n\n")
        exit(0) # Exit Cleanly
    except KeyboardInterrupt:
        destroy()
        DalekPrint( "\n\n............... Exit From KeYboard .......................\n\n")
        exit(0) # Exit Cleanly
    except Exception as inst:
        print(type(inst))
        print("\n................SOMETHING WENT WRONG!..................\n")
        
# End of __Main__ Startup Loop 
#======================================================================

