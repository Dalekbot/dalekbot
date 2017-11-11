#!/usr/bin/env python

#======================================================================
# Start of Main Imports and setup constants

# Module Imports
import RPi.GPIO as GPIO  # Import GPIO divers
import time              # Import the Time library

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
 
#TRIG = 40  # Set the Trigger pin
#ECHO = 38  # Set the Echo pin

# End of Main Imports and setup constants
#======================================================================

#======================================================================
# Initialisation procedures

def setup():                   # Setup GPIO and Initalise Imports
    connected = False
    while connected == False:
      #  connected = setupwii() # Setup and connect to WiiMote
    #GPIO.setmode(GPIO.BOARD)  # Set the GPIO pins as numbering - Set in DalekV2Drive.py
    GPIO.setwarnings(False)    # Turn GPIO warnings off - CAN ALSO BE Set in DalekV2Drive.py
    #GPIO.setup(TRIG,GPIO.OUT) # Set the Trigger pin to output
    #GPIO.setup(ECHO,GPIO.IN)  # Set the Echo pin to input
    DalekV2Drive.init()        # Initialise my software to control the motors
 
    # initialize the camera and grab a reference to the raw camera capture
    global hRes                # Allow Access to PiCam Horizontal Resolution
    global vRes                # Allow Access to PiCam Vertical Resolution

    # Setup WebCam
    global video_capture        # Allow Access to WebCam Object
    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, hRes)
    video_capture.set(4, vRes)

    print '\nPress some buttons!\n'                                     # Give instructions for connecting Wiimote
    print 'Press PLUS and MINUS together to disconnect and quit.\n'     # Give instructions for connecting Wiimote
  # End of Initialisation procedures
#======================================================================

#======================================================================
# Service Procedures
   
def getdistance(distance):
    GPIO.output(TRIG, False)
    print "Waiting For Sensor To Settle"
    time.sleep(0.05)
    pulse_end = 0

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        # print 'start', GPIO.input(ECHO)
        pulse_start = time.time()
  
    while GPIO.input(ECHO)==1:
        # print 'stop', GPIO.input(ECHO)
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    print "Distance:",distance,"cm"
    return distance
    
# ---- Function definition for converting scales ------
def remap(unscaled, to_min, to_max, from_min, from_max):
    return (to_max-to_min)*(unscaled-from_min)/(from_max-from_min)+to_min
    
# End of Service Procedures    
#======================================================================

#======================================================================
# Clean-up Procedures  
    
def destroy():                 # Shutdown GPIO and Cleanup modules

    global soundvolume         # Allow access to sound volume
        
    print "\n... Shutting Down...\n"
    scrollphat.clear()         # Shutdown Scroll pHat
    scrollphat.write_string("Ext")
    DalekV2Drive.stop()        # Make sure Bot is not moving when program exits
    DalekV2Drive.cleanup()     # Shutdown all motor control
    global wii                 # Allow access to the wii object
    wii.rumble = 1
    time.sleep(0.5)
    wii.rumble = 0
    volumesetting = '"--volume=' + str(soundvolume) +'"'
    subprocess.Popen(["mplayer",volumesetting, "Sound/Grow_stronger.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)
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

        print speed
        scrollphat.clear()         # Shutdown Scroll pHat
        scrollphat.write_string(str(speed))
        
        if boost == 0 and (buttons & cwiid.BTN_B):
            print 'Boost', maxspeed
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Max")
            savespeed = speed
            speed = maxspeed
            boost = 1
            time.sleep(.25)
        elif boost == 1 and (buttons & cwiid.BTN_B):
            speed = savespeed
            boost = 0
            print 'Normal', speed
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Nor")
            time.sleep(.25)
        
        if (buttons & cwiid.BTN_UP):
            print 'Forward', speed
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Fw")
            DalekV2Drive.forward(speed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_DOWN):
            print 'Backward', speed
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Bw")
            DalekV2Drive.backward(speed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_LEFT):
            print 'Spin Left', speed
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("SL")
            DalekV2Drive.spinLeft(maxspeed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_RIGHT):
            print 'Spin Right', speed
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("SR")
            DalekV2Drive.spinRight(maxspeed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_1):
            print 'Turn Right'
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("TrR")
            DalekV2Drive.turnForwardRight(outerturnspeed, innerturnspeed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_2):
            print 'Turn Left'
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("TrL")
            DalekV2Drive.turnForwardLeft(innerturnspeed, outerturnspeed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_PLUS):
            print 'Speed Up 1'
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("+1")
            if speed < 100:
                speed = speed + 1
                time.sleep(0.5)
        elif (buttons & cwiid.BTN_MINUS):
            print 'Speed Down 1'
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("-1")
            if speed > 0:
                speed = speed - 1
                time.sleep(0.5)
        elif (buttons & cwiid.BTN_A):
            print 'Stop'
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Stp")
            DalekV2Drive.stop()
            time.sleep(.25)
        elif (buttons & cwiid.BTN_HOME):
            DalekV2Drive.stop()
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Hm")
            print "\n\nReturning to Main Menu\n\n"
            time.sleep(1)
            print "Main Menu"               # Show we are on main menu
            print '\nUp    - ObstacleCourse'
            print 'Down  - StreightLine'
            print 'Left  - MinimaMaze'
            print 'Right - Golf'
            print '1     - Line Follow WebCam'
#            print '2     - Line Follow PiCam'
            print 'Home  - Exit\n'
            print "Ready"
            break
    
#def StreightLine():
    
#def MinimuMaze():

#def Golf():

def LineFollowWebCam(showcam):

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
    
    print'\nPress "A" to start Line following'
    print'Press "Hm" to return to main menu\n'
        
    scrollphat.clear()         # Shutdown Scroll pHat
    scrollphat.write_string('"A"')
    time.sleep(.25)

    while True:
    
        buttons = wii.state['buttons']          # Get WiiMote Button Pressed

        if (buttons & cwiid.BTN_A):
            print 'Start Line Following'
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('LiF')
            time.sleep(.25)
            cx = 300                   # Go Streight
            
            while True:
            
                buttons = wii.state['buttons']          # Get WiiMote Button Pressed
                # Choose which task to do
                if (buttons & cwiid.BTN_HOME):
                    DalekV2Drive.stop()
                    print'\nPress "A" to start Line following'
                    print'Press "Hm" to return to main menu\n'
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
                    print "Turn Right: ", SteerRight, cx
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string("TrR")
                    DalekV2Drive.spinRight(turnspeed)

                # --------- On Track Routine ----------
                if cx < 370 and cx > 270:
                    print "On Track", cx
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string("Fw")
                    DalekV2Drive.forward(speed)

                # --------- Steer Left Routine ----------
                if cx <= 270:
                    LSteer = 270 - cx
                    SteerLeft = remap(LSteer, 0, 45, 1, 270)
                    print "Turn Left: ", SteerLeft, cx
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string("TrL")
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
            print "\n\nReturning to Main Menu\n\n"
            time.sleep(1)
            print "Main Menu"               # Show we are on main menu
            print '\nUp    - ObstacleCourse'
            print 'Down  - StreightLine'
            print 'Left  - MinimaMaze'
            print 'Right - Golf'
            print '1     - Line Follow WebCam'
#            print '2     - Line Follow PiCam'
            print 'Home  - Exit\n'
            print "Ready"
            break

            
# End of Task Procedures  
#======================================================================    

#======================================================================    
# Main Control Procedure
    
def maincontrol(showcam):                  # Main Control Loop

    global wii                      # Allow access to 'Wii' constants
    global soundvolume              # Allow access to sound volume

    scrollphat.clear()              # Clear Scroll pHat
    scrollphat.write_string("Mn")   # Show we are on main menu
    print "Main Menu"               # Show we are on main menu

    print '\nUp    - ObstacleCourse'
    print 'Down  - StreightLine'
    print 'Left  - MinimaMaze'
    print 'Right - Golf'
    print '1     - Line Follow WebCam'
#    print '2     - Line Follow PiCam'
    print 'Home  - Exit\n'
    
    wii.rpt_mode = cwiid.RPT_BTN

    print "Ready"
    
    while True:
    
        scrollphat.clear()              # Clear Scroll pHat
        scrollphat.write_string("Mn")   # Show we are on main menu

        buttons = wii.state['buttons']          # Get WiiMote Button Pressed
        # Choose which task to do
     
        # If Plus and Minus buttons pressed
        # together then rumble and quit.
        if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):  
            break  
 
        if (buttons & cwiid.BTN_UP):
            print 'ObstacleCourse'
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string("OC")
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(["mplayer",volumesetting, "Sound/Rant.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ObstacleCourse()
        elif (buttons & cwiid.BTN_DOWN):
            print 'StreightLine'
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string("StL")
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(["mplayer",volumesetting, "Sound/Stay.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)
            #StreightLine()
        elif (buttons & cwiid.BTN_LEFT):
            print 'MinimalMaze'
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string("MM")
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(["mplayer",volumesetting, "Sound/IntruderLocated.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)
            #MinimalMaze()
        elif (buttons & cwiid.BTN_RIGHT):
            print 'Golf'
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string("Golf")
            time.sleep(1)
            #ObstacleCourse()
        elif (buttons & cwiid.BTN_1):
            print 'Line Follow WebCam'
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string("LiF")
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(["mplayer",volumesetting, "Sound/IntruderLocated.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            LineFollowWebCam(showcam)
#        elif (buttons & cwiid.BTN_2):
#            print 'Line Follow PiCam'
#            scrollphat.clear()         # Clear Scroll pHat
#            scrollphat.write_string("LiF")
#            LineFollowPiCam(showcam)
        elif (buttons & cwiid.BTN_PLUS):
            print '+'
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string("+")
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(["mplayer",volumesetting, "Sound/exterminate.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif (buttons & cwiid.BTN_MINUS):
            print '-'
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string("-")
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
        print '\nRight Speed - ',(str(args.RightSpeed))
        rightspeed = args.RightSpeed

    if ((str(args.LeftSpeed)) != 'None'):
        print 'Left Speed - ',(str(args.LeftSpeed))
        leftspeed = args.LeftSpeed

    if ((str(args.Speed)) != 'None'):
        print '\nGeneral Speed - ',(str(args.Speed))
        speed = args.Speed
    
    if ((str(args.Brightness)) != 'None'):
        print '\nscrollpHat Brightness - ',(str(args.Brightness))
        scrollphat.set_brightness(int(args.Brightness))

    if ((str(args.InnerTurnSpeed)) != 'None'):
        print '\nInner Turn Speed - ',(str(args.InnerTurnSpeed))
        innerturnspeed = args.InnerTurnSpeed
    
    if ((str(args.OuterTurnSpeed)) != 'None'):
        print '\nOuter Turn Speed - ',(str(args.OuterTurnSpeed))
        outerturnspeed = args.OuterTurnSpeed
 
    if ((str(args.ShowCam)) != 'None'):
        print '\nShow Cam Image - ',(str(args.ShowCam))
        showcam = args.ShowCam
    else:
        showcam = False

    if ((str(args.SoundVolume)) != 'None'):
        print '\nSound Volume - ',(str(args.SoundVolume))
        soundvolume = args.SoundVolume
    else:
        soundvolume = 100
        print '\nSound Volume - ',soundvolume
        
    print '\n\nSetting Up ...\n'
    scrollphat.clear()         # Clear Scroll pHat
    scrollphat.write_string("Set")
    
    volumesetting = '"--volume=' + str(soundvolume) +'"'
    subprocess.Popen(["mplayer",volumesetting, "Sound/Beginning.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    setup()           # Setup all motors and Wii

    print '\nGo ...\n\n'
    scrollphat.clear()         # Clear Scroll pHat
    scrollphat.write_string("Go")
	
    try:
        maincontrol(showcam)    # Call main loop
        destroy()     # Shutdown
        print "\n\n................... Exit .......................\n\n"
        exit(0) # Exit Cleanly
    except KeyboardInterrupt:
        destroy()
        print "\n\n................... Exit .......................\n\n"
        exit(0) # Exit Cleanly
        
# End of __Main__ Startup Loop 
#======================================================================

