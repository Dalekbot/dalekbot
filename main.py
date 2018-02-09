#!/usr/bin/env python3

# style guide https://google.github.io/styleguide/pyguide.html

import sys
sys.settrace
import os
from operator import itemgetter
#======================================================================
# Start of Main Imports and setup constants

# Module Imports
import RPi.GPIO as GPIO          # Import GPIO divers
import time                      # Import the Time library
import argparse                  # Import Argument Parser
import numpy as np               # Import NumPy Array manipulation
# import cv2                       # Import OpenCV Vision code
from dalek import drive          # Import the 4 Motor controller
# Import the debug module that also prints to the robots output device
from dalek import debug
from dalek import spi            # Import the Spi Raspi to Arduino libray
from dalek import sound_player   # Import the mp3 player module
from dalek import controller     # Import the PS3 controller
from dalek import settings

# Main Imports and setup constants
dalek_settings = settings.Settings()
dalek_sounds = sound_player.Mp3Player(True)  # initialize the sound player

# End of Main Imports and setup constants
#======================================================================

#======================================================================
# Initialization procedures


def setup():                   # Setup GPIO and initialize Imports

    debug.turn_debug_on()                  # use the debug and turn on output
    # if left empty then default is just stout
    debug.set_output_device("scrollphat")

    dalek_sounds.set_volume_level(-5)     # values: -20 to 10
    dalek_sounds.play_sound("Beginning")  # annoy someone

    # Set the GPIO pins as numbering - Also set in drive.py
    GPIO.setmode(GPIO.BOARD)
    # Turn GPIO warnings off - CAN ALSO BE Set in drive.py
    GPIO.setwarnings(False)

    drive.init()               # Initialise the software to control the motors
    spi.init()                 # Initialise my software for the MOSI/spi Bus
    controller.init()          # Initialise the controller

    # this should not be needed as we are only using the value not rebinding a new value to it.
    # initialize the camera and grab a reference to the raw camera capture
    # global hRes                # Allow Access to PiCam Horizontal Resolution
    # global vRes                # Allow Access to PiCam Vertical Resolution

    # # Setup WebCam
    # global video_capture        # Allow Access to WebCam Object
    # video_capture = cv2.VideoCapture(0)
    # video_capture.set(3, hRes)
    # video_capture.set(4, vRes)


# End of Initialization procedures
#======================================================================
# Clean-up Procedures

def destroy():                 # Shutdown GPIO and Cleanup modules

             # Allow access to sound volume
    global dalek_sounds

    debug.print_to_all_devices("\n... Shutting Down...\n", "Ext")
    dalek_sounds.play_sound("Grow_stronger")
    drive.stop()        # Make sure Bot is not moving when program exits
    drive.cleanup()     # Shutdown all motor control
    # time.sleep(2)
#    cv2.destroyAllWindows()    # Shutdown any open windows
    # time.sleep(1.5)
    debug.destroy()        # Clear Scroll pHat
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


def maincontrol():                  # Main Control Loop
    controller.use(dalek_settings, dalek_sounds)

# End of Main Control Procedure
#======================================================================

#======================================================================
# __Main__ Startup Loop


if __name__ == '__main__':  # The Program will start from here

    # Get and parse Arguments
    parser = argparse.ArgumentParser(
        description='PiWars Dalek Control Program')
    # Initial speed of Right Motors
    parser.add_argument('-r', dest='RightSpeed', type=float,
                        help='Initial speed of Right motors (0 - 100)')
    # Initial speed of Left Motors
    parser.add_argument('-l', dest='LeftSpeed', type=float,
                        help='Initial speed of Left Motors (0 - 100)')
    # Initial General speed of Motors
    parser.add_argument('-s', dest='Speed', type=float,
                        help='Initial General speed of Motors (0 - 100)')
    # Brightness of scrollpHat
    parser.add_argument('-b', dest='Brightness', type=float,
                        help='Brightness of scrollpHat (0 - 5)')
    parser.add_argument('-i', dest='InnerTurnSpeed', type=float,
                        help='Speed of Inner wheels in a turn (0 - 100)')  # Speed of Inner wheels in a turn
    parser.add_argument('-o', dest='OuterTurnSpeed', type=float,
                        help='Speed of Inner wheels in a turn (0 - 100)')  # Speed of Outer wheels in a turn
    # Show Image from Active Cam
    parser.add_argument('-c', dest='ShowCam', type=bool,
                        help='Show Image from Active Cam (True/False)')
    # Set Sound Volume
    parser.add_argument('-v', dest='SoundVolume', type=int,
                        help='Set Sound volume (0 - 100)')
    args = parser.parse_args()

    if ((str(args.RightSpeed)) != 'None'):
        debug.print_to_all_devices(
            "\nRight Speed - {}".format(args.RightSpeed))
        dalek_settings.right_speed = args.RightSpeed

    if ((str(args.LeftSpeed)) != 'None'):
        debug.print_to_all_devices("\nLeft Speed - {}".format(args.LeftSpeed))
        dalek_settings.left_speed = args.LeftSpeed

    if ((str(args.Speed)) != 'None'):
        debug.print_to_all_devices("\nGeneral Speed - {}".format(args.Speed))
        dalek_settings.speed = args.Speed

    if ((str(args.Brightness)) != 'None'):
        debug.print_to_all_devices(
            "\nscrollpHat Brightness - {}".format(args.Brightness))
        DalekDebugSetBrightness(int(args.Brightness))

    if ((str(args.InnerTurnSpeed)) != 'None'):
        debug.print_to_all_devices(
            "\nInner Turn Speed - {}".format(args.InnerTurnSpeed))
        dalek_settings.inner_turn_speed = args.InnerTurnSpeed

    if ((str(args.OuterTurnSpeed)) != 'None'):
        debug.print_to_all_devices(
            "\nOuter Turn Speed - {}".format(args.OuterTurnSpeed))
        dalek_settings.outer_turn_speed = args.OuterTurnSpeed

    if ((str(args.ShowCam)) != 'None'):
        debug.print_to_all_devices(
            "\nShow Cam Image - {}".format(args.ShowCam))
        dalek_settings.show_cam = args.ShowCam  # default is False

    if ((str(args.SoundVolume)) != 'None'): 
        debug.print_to_all_devices(
            "\nSound Volume - {}".format(args.SoundVolume))
        dalek_settings.sound_volume = args.SoundVolume  # default is 0

    debug.print_to_all_devices("\n\nSetting Up ...", "Set")

    setup()           # Setup all motors
    # debug.print_to_all_devices("\nGo ...\n\n", "Go")

    try:
        # debug.print_to_all_devices("OK 1")
        maincontrol()    # Call main loop
        # debug.print_to_all_devices("OK 2")

        destroy()     # Shutdown
        print("\n... Exit ...\n")
        exit(0)  # Exit Cleanly
    except KeyboardInterrupt:
        destroy()
        print("\n... Exit From Keyboard ...\n")
        exit(0)  # Exit Cleanly
    except Exception as inst:
        print(type(inst))
        print("\n... SOMETHING WENT WRONG! ...\n")

# End of __Main__ Startup Loop
#======================================================================
