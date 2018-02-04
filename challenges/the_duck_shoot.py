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
   import RPi.GPIO as GPIO          # Import GPIO divers

import time
# from dalek import spi
from dalek import drive
from dalek import debug
import threading


# it needs to run in a thread otherwise the joystick can not run at the same time


class Challange(threading.Thread):
    def __init__(self, dalek_settings, dalek_sounds):
      super().__init__()
      self.running = False
      self.dalek_settings = dalek_settings
      self.dalek_sounds = dalek_sounds

    def run(self):
      self.running = True
      debug.print_to_all_devices("Challange the duck shoot is now running")
      while self.running:

        ####################################################
        #                                                  #
        # Code for this challange goes in this while loop  #
        #                                                  #
        ####################################################
        debug.print_to_all_devices("bang!!")  # this line can be removed
        time.sleep(2)                         # this line can be removed
    
    def stop_runnning(self):
        '''
        when this is called it ends this thread
        '''
        self.running = False
    
    def cross_button_pressed(self):
      debug.print_to_all_devices("x_button_pressed()")
    
    def circle_button_pressed(self):
      debug.print_to_all_devices("circle_button_pressed()")
    
    def triangle_button_pressed(self):
      debug.print_to_all_devices("triangle_button_pressed()")
    
    def square_button_pressed(self):
      debug.print_to_all_devices("square_button_pressed()")
    






def main(dalek_settings, dalek_sounds):
    
    challange = Challange(dalek_settings, dalek_sounds)
    challange.start()
    challange.join() # wait for thead to finish.
    debug.print_to_all_devices("\nFINISHED")



if __name__ == "__main__":
    debug.debug_on = True
    dalek_settings = settings.Settings()
    dalek_sounds = sound_player.Mp3Player(True) # initialize the sound player
    main(dalek_settings, dalek_sounds)

else:
    debug.print_to_all_devices('importing duck Shoot')