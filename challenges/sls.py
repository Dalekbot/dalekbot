if __name__ == "__main__":
    '''
    This if statement is needed for testing, to locate the modules needed
    if we are running the file directly.
    '''
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from dalek import settings
    # from dalek import sound_player
    import RPi.GPIO as GPIO          # Import GPIO divers

import time
from dalek import spi
from dalek import drive


driving = True

def start(dalek_settings):
    arduino_sensor_data = spi.SensorData()
    arduino_sensor_data.start()  # starts the new process and runs in the background
    time.sleep(0.2)

    while True:
           '''
           TODO:
           The dalek_settings.drive can be turned off with the controller 
           ''' 
   
           drive.forward(100)
   
           # detects we have finished the challenge.
           if arduino_sensor_data.front_distance<= 10:
               drive.cleanup()
               print("Center Distance:{}cm Run Finished"
                                          .format(arduino_sensor_data.front_distance))
               arduino_sensor_data.running = False
               break
   
           if arduino_sensor_data.left_distance <= 5:
               print("turnForwardRight", "TrR")
               drive.turnForwardRight(dalek_settings.outer_turn_speed,
                                      dalek_settings.inner_turn_speed)
               time.sleep(.1)
               drive.forward(dalek_settings.max_speed)
   
           if arduino_sensor_data.right_distance <= 5:
               print("turnForwardLeft", "TrL")
               drive.turnForwardLeft(dalek_settings.inner_turn_speed,
                                     dalek_settings.outer_turn_speed)
               time.sleep(.1)
               drive.forward(dalek_settings.max_speed)
   
          # wait for process to  finish
           print("Done...")
   
def main():
   # '''
   # This is only run if you run the file directly
    #'''

    GPIO.setmode(GPIO.BOARD)   # Set the GPIO pins as numbering - Also set in drive.py
    GPIO.setwarnings(False)
    drive.init()
    spi.init()
    dalek_settings = settings.Settings()
    dalek_settings.slow_mode()

    dalek_settings
    # try:
    start(dalek_settings)
    #     time.sleep(1)
    # except:
    #     print("!!! error")
    # drive.cleanup()


if __name__ == "__main__":
    main()
else:
    print('not main')
