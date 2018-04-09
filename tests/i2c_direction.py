if __name__ == "__main__":
    '''
    This if statement is needed for testing, to locate the modules needed
    if we are running the file directly.
    '''
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import time
from  dalek import spi 
from dalek import drive 
from dalek import head_controller

import RPi.GPIO as GPIO  # Import GPIO divers

GPIO.setwarnings(False)


# drive.init()
spi.init()





def main():
    # sensorData = spi.SensorData()
    # sensorData.start()
    Compass = spi.CompassData()
    Compass.start()

    
    time.sleep(5)


    Compass.stop_running()
    # # time.sleep(1)
    # # print("1")
    # head_controller.leds_change_color(head_controller.leds_color['red'])
    # # print("2")
    # head_controller.head_move_to_center()
    # print("center mag:{}" .format(sensorData.compass))
    # print("center mag:{}" .format(spi.get_mag()))
    # print("laser center:{}" .format(sensorData.laser_center))
    # time.sleep(1)
    # # print("3")
    # head_controller.head_move_left_90deg()
    # time.sleep(2)
    # print("left mag:{}" .format(sensorData.compass))
    # print("left mag:{}" .format(spi.get_mag()))
    # time.sleep(.5)

    # head_controller.head_move_right_90deg()
    # time.sleep(2)
    # print("right mag:{}" .format(sensorData.compass))
    # print("right mag:{}" .format(spi.get_mag()))
    # # print("4")
    # head_controller.leds_change_color(head_controller.leds_color['white'])
    # # print("5")
    # head_controller.head_move_to_center()
    # time.sleep(1)

    # sensorData.stop_running()






if __name__ == "__main__": 
    main()
    # drive.stop()
    # drive.cleanup()