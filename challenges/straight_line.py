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

# these are the globaly used modules
from challenges import challenge
import time
from dalek import spi
from dalek import drive
from dalek import debug


class Challenge(challenge.ChallengeBase):
    '''
    Do Not change the class name, it is called in the controller.py.
    The buttons can be overridden if you need to add functionally to them.
    The main loop is the run() function, all code goes in it.

    Look at the ChallengeBase class in challenge.py for all functions that can be called.
    '''
    def __init__(self,dalek_settings, dalek_sounds):
        super().__init__()
        
        self.dalek_settings = dalek_settings
        self.dalek_sounds = dalek_sounds
        self.arduino_sensor_data = spi.SensorData()
        # self.
        
    def stop_runnning(self):
        '''
        When this is called it ends this thread 
        This is also called if the PS3 button is pressed during a challenge,
        so add any cleanup code here.
        '''
        drive.stop()
        if self.arduino_sensor_data.is_alive():
            self.arduino_sensor_data.stop_runnning()
            self.arduino_sensor_data.join() ## wait for process to  finish
        self.running = False   
        debug.print_to_all_devices("Done...")
    
    def run(self):
      self.running = True
      debug.print_to_all_devices("Challenge 'Straight line' Started." )
      # self.arduino_sensor_data.start() #   starts the new process and runs in the background

      
      self.arduino_sensor_data.start()
      time.sleep(0.2)

      

      while self.running:
        drive.forward(self.dalek_settings.max_speed)
        time.sleep(.1)
        
        # # detects we have finished the challenge. 
        if self.arduino_sensor_data.frontPing <= 18:
            drive.stop()
            debug.print_to_all_devices("Center Distance:{}cm Run Finished"
                                    .format(self.arduino_sensor_data.frontPing))
            self.stop_runnning()
            
            
 
        if self.arduino_sensor_data.leftPing <= 5:
            debug.print_to_all_devices("turnForwardRight", "TrR" )
            drive.turnForwardRight(self.dalek_settings.outer_turn_speed,
                                        self.dalek_settings.inner_turn_speed)
            time.sleep(.05)
            drive.forward(self.dalek_settings.max_speed)
        

        if self.arduino_sensor_data.rightPing <= 5:
            debug.print_to_all_devices("turnForwardLeft", "TrL" )
            drive.turnForwardLeft(self.dalek_settings.inner_turn_speed,
                                        self.dalek_settings.outer_turn_speed)
            time.sleep(.05)
            drive.forward(self.dalek_settings.max_speed) 

      
          





def main(): 
    pass
    # pass
    # GPIO.setmode(GPIO.BOARD)   # Set the GPIO pins as numbering - Also set in drive.py
    # GPIO.setwarnings(False) 

    # debug.debug_on = True
    # dalek_settings = settings.Settings()
    # dalek_settings.slow_mode()

    # spi.init()

    # drive.init()
    # dalek_sounds = sound_player.Mp3Player(True) # initialize the sound player
   


    # challenge = Challenge(dalek_settings, dalek_sounds)
    # challenge.start()
    # # time.sleep(4)
    # # challenge.button_circle_pressed()
    # # challenge.stop_runnning()

    # challenge.join() # wait for thead to finish.
    # debug.print_to_all_devices("\nFINISHED")
    

    



if __name__ == "__main__":
    main()
   

else:
    debug.print_to_all_devices('importing Straight Line Challenge')