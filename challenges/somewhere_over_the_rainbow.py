if __name__ == "__main__":
   '''
   This if statement is needed for testing, to locate the modules needed
   if we are running the file directly.
   '''
   import sys
   from os import path
   sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
   from dalek import settings
   from dalek import sound_player
   import RPi.GPIO as GPIO

# these are the globally used modules
import os
from challenges import challenge
import time
# from dalek import spi
from dalek import drive
from dalek import debug

import numpy as np       # Import NumPy Array manipulation
import cv2               # Import OpenCV Vision code
from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera

video_capture = 0        
video_capture = picamera.PiCamera()

hRes = 320
vRes = 240

print ("default resolution = " + str(video_capture.resolution))
video_capture.resolution = (hRes,vRes)
print ("updated resolution = " + str(video_capture.resolution))
video_capture.framerate = 32
video_capture.hflip = True
rawCapture = PiRGBArray(video_capture, size=(hRes, vRes))
# allow the camera to warmup
time.sleep(0.1)


class Challenge(challenge.ChallengeBase):
    '''
    Do Not change the class name, it is called in the controller.py.
    The buttons can be overridden if you need to add functionally to them.
    The main loop is the run() function, all code goes in it.

    Look at the ChallengeBase class in challenge.py for all functions that can be called.
    '''

    def __init__(self, dalek_settings, dalek_sounds):
        super().__init__()
        self.dalek_settings = dalek_settings
        self.dalek_sounds = dalek_sounds

    def run(self):
        self.running = True
        debug.print_to_all_devices(
            "Challenge 'somewhere over the rainbow")





        if video_capture._check_camera_open() == False:                           # check if VideoCapture object was associated to webcam successfully
            print ("error: capWebcam not accessed successfully\n\n")          # if not, print error message to std out
            os.system("pause")                                              # pause until user presses a key so user can see error message
            self.running= False # ruturns 

        intXFrameCenter = int(float(hRes) / 2.0)
        intYFrameCenter = int(float(vRes) / 2.0)
        



        if intXFrameCenter == 0.0:
            # scrollphat.clear()         # Shutdown Scroll pHat
            # scrollphat.write_string('Err')
            time.sleep(2)
            self.running= False # ruturns
     
        panServoPosition = intXFrameCenter

        # print ('\nPress "A" to Chase the Rainbow')
        # print ('Press "Hm" to return to main menu\n')
            
        # scrollphat.clear()         # Shutdown Scroll pHat
        # scrollphat.write_string('"A"')
        
        time.sleep(.25)

####################################################
#                                                  #
# Code for this challenge goes in this while loop  #
#    call    self.running= False to exit challenge #
####################################################
        while self.running:

            debug.print_to_all_devices("rainbow start ")  # this line can be removed
            # this line can be removed
            time.sleep(2)
  





####################################################
#                                                  #
# END   of main loop                               #
#                                                  #
####################################################

def main(dalek_settings, dalek_sounds):
    # pass
    challenge = Challenge(dalek_settings, dalek_sounds)
    challenge.start()
    time.sleep(2) 
    # challenge.button_circle_pressed()
    challenge.stop_running()

    # challenge.join() # wait for thread to finish.
    debug.print_to_all_devices("\nFINISHED")
    drive.cleanup()


if __name__ == "__main__":
    # pass
    GPIO.setwarnings(False)
    drive.init()
    debug.debug_on = True
    dalek_settings = settings.Settings()
    dalek_sounds = sound_player.Mp3Player(True) # initialize the sound player
    main(dalek_settings, dalek_sounds)

else:
    debug.print_to_all_devices('importing slightly_deranged_golf Challenge')
