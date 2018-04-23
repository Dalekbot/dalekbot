if __name__ == "__main__":
    '''
    This if statement is needed for testing, to locate the modules needed
    if we are running the file directly.
    '''
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from dalek import settings
    from dalek import sound_player
    import RPi.GPIO as GPIO          # Import GPIO divers

import time
from dalek import spi
from dalek import drive
from dalek import debug

# The original file has been put in obsolete_files folder
# This is just to get things going


def straight_line_speed_test(dalek_settings, dalek_sounds):
    arduino_sensor_data = spi.SensorData()
    arduino_sensor_data.start()  # starts the new process and runs in the background
    time.sleep(0.2)
    start_button = False

    def button_start_pressed():
        print("from straighe line challenge")


    while dalek_settings.drive:
        '''
        TODO:
        The dalek_settings.drive can be turned off with the controller 
        ''' 

        drive.forward(dalek_settings.max_speed)

        # detects we have finished the challenge.
        if arduino_sensor_data.front_distance<= 10:
            drive.cleanup()
            debug.print_to_all_devices("Center Distance:{}cm Run Finished"
                                       .format(arduino_sensor_data.frontPing))
            arduino_sensor_data.running = False
            break

        if arduino_sensor_data.left_ping <= 5:
            debug.print_to_all_devices("turnForwardRight", "TrR")
            drive.turnForwardRight(dalek_settings.outer_turn_speed,
                                   dalek_settings.inner_turn_speed)
            time.sleep(.1)
            drive.forward(dalek_settings.max_speed)

        if arduino_sensor_data.right_distance <= 5:
            debug.print_to_all_devices("turnForwardLeft", "TrL")
            drive.turnForwardLeft(dalek_settings.inner_turn_speed,
                                  dalek_settings.outer_turn_speed)
            time.sleep(.1)
            drive.forward(dalek_settings.max_speed)

    arduino_sensor_data.join()  # wait for process to  finish
    debug.print_to_all_devices("Done...")


def straight_line_speed_test_1(dalek_settings, dalek_sounds):
    '''
    finds the middle of the area and drives down it.
    '''
    arduino_sensor_data = spi.SensorData()
    arduino_sensor_data.start()  # starts the new process and runs in the background
    time.sleep(0.2)

    turning_left = False
    turning_right = False
    previous_center_value = arduino_sensor_data.left_ping - arduino_sensor_data.right_distance
    counter = 0


    while dalek_settings.drive:
        '''
        TODO:
        The dalek_settings.drive can be turned off with the controller 
        '''

        drive.forward(dalek_settings.max_speed)
        time.sleep(.5)

        # detects we have finished the challenge.
        if arduino_sensor_data.frontPing <= 10:
            drive.cleanup()
            debug.print_to_all_devices("Center Distance:{}cm Run Finished"
                                       .format(arduino_sensor_data.frontPing))
            arduino_sensor_data.running = False
            break

        center_value = arduino_sensor_data.left_ping - arduino_sensor_data.right_distance
        print(center_value)

        # if  (center_value - 1) <= previous_center_value <= (center_value + 1) :
        if previous_center_value == center_value:
            # use the if between to stop hunting, a few centermeters either way
            #  should be fine.
            # we are driving parallel to walls
            # we should be able to drive forward while moving into the middle.
            print("parallel to walls {} {}".format(
                previous_center_value, center_value))

        else:
            print("Not parallel to walls {} {}".format(
                previous_center_value, center_value))

        counter += 1
        if counter == 10:
            previous_center_value = center_value
            counter = 0

        # print(counter)

        if (center_value < -2) and turning_right == False:
            turning_right = True
            turning_left = False
            drive.turnForwardRight(dalek_settings.outer_turn_speed,
                                   dalek_settings.inner_turn_speed)
            debug.print_to_all_devices("turnForwardRight", "TrR")
            time.sleep(.05)
            # drive.forward(dalek_settings.max_speed)
            # time.sleep(.05)

        if (center_value > 2) and turning_left == False:
            turning_left = True
            turning_right = False
            drive.turnForwardLeft(dalek_settings.inner_turn_speed,
                                  dalek_settings.outer_turn_speed)
            debug.print_to_all_devices("turnForwardLeft", "TrL")
            time.sleep(.05)
            # drive.forward(dalek_settings.max_speed)
            # time.sleep(.05)

        # if  -2 <= center_value <= 2:
        #     # if it is between these values
        #     # straiten up the bot
        #     if turning_left

    arduino_sensor_data.join()  # wait for process to  finish
    debug.print_to_all_devices("Done...")


def drive_back(dalek_settings, time_to_drive):
    '''
       used when testing so you dont have to keep getting up.
    '''
    debug.print_to_all_devices("Start drive back")
    drive.backward(50)
    time.sleep(time_to_drive)
    debug.print_to_all_devices("end drive back")


def main():
    '''
    This is only run if you run the file directly
    '''
    GPIO.setmode( GPIO.BOARD)   # Set the GPIO pins as numbering - Also set in drive.py
    GPIO.setwarnings(False)
    spi.init()
    dalek_settings = settings.Settings()
    dalek_settings.slow_mode()
    drive.init()
    dalek_sounds = sound_player.Mp3Player(True)  # initialize the sound player
    debug.debug_on = True
    debug.print_to_all_devices("working", "OK")
    try:
        straight_line_speed_test(dalek_settings, dalek_sounds)
        time.sleep(1)
    except:
        print("!!! error")
        drive.cleanup()

    # try:
    #     drive_back(dalek_settings,2)
    # except expression as identifier:
    #     pass


if __name__ == "__main__":
    main()
else:
    print('not main')
