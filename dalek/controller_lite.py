if __name__ == "__main__":
    '''
    This if statement is needed for testing, to locate the modules needed
    if we are running the file directly.
    '''
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    import RPi.GPIO as GPIO

import os.path
import struct
import time
from dalek import drive
from dalek import head_controller
from dalek import debug


def init():
    head_controller.leds_change_color(head_controller.leds_color['red'])
    head_controller.leds_flash()
    fn = '/dev/input/js0'

    debug.print_to_all_devices("Testing for joystick: {}...".format(fn))

    file_exists = False
    while file_exists == False:

        file_exists = os.path.exists(fn)
        debug.print_to_all_devices(
            'joystick paired: {} '.format(os.path.exists(fn)))
        time.sleep(3)

    jsdev = open(fn, 'rb')


def start(speed=80):
    head_controller.leds_change_color(head_controller.leds_color['green'])

    current_challenge = 1

    # used for the main loop, when set to false this function ends.
    using_controller = True
    button_select_status = True
    button_start_status = False

    jsdev = open("/dev/input/js0", 'rb')

    joystickD_padCurrentButton = 0  # used for debounce of switches on d_pad.

    # if set to false thumbsticks do not work
    tank_drive_on = True
    leftPaddle = 0   # raw axis data
    rightPaddle = 0  # raw axis data

    # animation of head
    # lets us know things are ok
    head_controller.head_no()
    # head_controller.head_move_to_center()
    head_controller.eye_move_to_center()
    head_controller.leds_flash(False)

    def check_for_finished_using_controller():
        '''
        If BOTH the select and the start buttons are pressed down together at same time,
        then we end the main loop and return out of the function.
        '''
        nonlocal using_controller  # , controller_battery_monitor
        if (button_select_status == True) and (button_start_status == True):

            try:
                os.system('clear')
                # stop_current_challenge()

            except:
                print("error shutting down")

            using_controller = False

    ###########################################################
    ###  DPad Buttons on ps3 controller (Left hand buttons) ##
    ###########################################################

    def dpad_up_button_pressed():
            # drive.forward(speed)
        head_controller.eye_move_to_top()

    # def dpad_up_button_released():
    #     head_controller.eye_stop()

    def dpad_down_button_pressed():
        # drive.backward(speed)
        head_controller.eye_move_to_bottom()

    # def dpad_down_button_released():
    #     head_controller.eye_stop()

    def dpad_right_button_pressed():
        # drive.spinRight(speed)
        head_controller.head_move_right_90deg()

    # def dpad_right_button_released():
    #     head_controller.head_stop()

    def dpad_left_button_pressed():
        # drive.spinLeft(speed)
        head_controller.head_move_left_90deg()

    # def dpad_left_button_released():
    #     head_controller.head_stop()

    # do not change below use the functions above.
    def dpad_button_pressed(value, number, _joystickD_padCurrentButton):
        if (value == 0) and (number == _joystickD_padCurrentButton):
            drive.stop()

        # Up button
        else:
            if number == 4:
                
                if value:  # value is 1 for pressed 0 for released.
                    dpad_up_button_pressed()
                # else:
                #     dpad_up_button_released()

            # Right button
            elif number == 5:
                if value:
                    dpad_right_button_pressed()
                else:
                    dpad_right_button_released()

            # Down button
            elif number == 6:
                if value:
                    dpad_down_button_pressed()
                else:
                    dpad_down_button_released()

            # Left button
            elif number == 7:
                if value:
                    dpad_left_button_pressed()
                else:
                    dpad_left_button_released()

    def tank_drive(_leftPaddle, _rightPaddle):
        debug.print_to_all_devices(
            "left: {}  Right: {}".format(_leftPaddle, _rightPaddle))

        if (_leftPaddle == 0) and (_rightPaddle == 0):
            drive.stop()
            debug.clear()
        elif (_leftPaddle < 0) and (_rightPaddle < 0):
            drive.paddleForward(- _leftPaddle, - _rightPaddle)
            # debug.print_to_all_devices("forwards","Fw")
        elif (_leftPaddle > 0) and (_rightPaddle > 0):
            drive.paddleBackward(_leftPaddle, _rightPaddle)
            # debug.print_to_all_devices("Backwards", "Bw")
        elif (_leftPaddle <= 0) and (_rightPaddle >= 0):
            drive.turnForwardRight(- _leftPaddle,  _rightPaddle)
            # debug.print_to_all_devices("Spin Right", "SR")
        elif (_leftPaddle >= 0) and (_rightPaddle <= 0):
            drive.turnForwardLeft(_leftPaddle, - _rightPaddle)
            # debug.print_to_all_devices("Spin Left", "SL")

    ###########################################################
    ###  Symbol Buttons on the Controller                    ##
    ###########################################################
    def button_circle_pressed():
        print("circle Pressed")

    def button_circle_released():
        pass

    def button_square_pressed():
        print("square Pressed")
        head_controller.leds_cycle_colors()

    def button_square_released():
        pass

    def button_triangle_pressed():
        print("triangle Pressed")
        head_controller.leds_toggle_flash()

    def button_triangle_released():
        pass

    def button_cross_pressed():
        print("cross Pressed")
        pass

    def button_cross_released():
        pass

    ###########################################################
    ###  Lower Buttons on the Controller                      ##
    ###########################################################
    def button_L1_pressed():
        head_controller.head_move_left_90deg()
        print("l1 Pressed")

    def button_L1_released():
        head_controller.head_stop()

    def button_L2_pressed():

        head_controller.eye_move_to_bottom()
        print("l2 Pressed")

    def button_L2_released():
        head_controller.eye_stop()

    def button_R1_pressed():
        head_controller.head_move_right_90deg()
        print("R1 Pressed")

    def button_R1_released():
        head_controller.head_stop()

    def button_R2_pressed():
        head_controller.eye_move_to_top()
        print("R2 Pressed")

    def button_R2_released():
        head_controller.eye_stop()

     ###########################################################
    ###  Main Buttons on the Controller                      ##
    ###########################################################

    def button_select_pressed():
        nonlocal button_select_status, tank_drive_on

        # uses for shuting down the program safely
        button_select_status = True
        check_for_finished_using_controller()

    def button_select_released():
        nonlocal button_select_status
        button_select_status = False

        return 1  # resets ps3_ControllerMode  to Drive Mode

    def button_start_pressed():
        nonlocal button_start_status
        button_start_status = True
        check_for_finished_using_controller()

    def button_start_released():
        nonlocal button_start_status
        button_start_status = False

    def button_PS3():
        nonlocal tank_drive_on
        pass

    ###########################################################
    ###  paddle Buttons on the Controller                    ##
    ###########################################################
    def button_left_paddle():
        # debug.print_to_all_devices("Left Paddle Button Pressed")
        head_controller.leds_cycle_colors()

    def button_right_paddle():
        # debug.print_to_all_devices("Right Paddle Button Pressed")
        head_controller.leds_toggle_flash()

    #####################################################################
    ###                            Main loop                           ##
    ###  this is where we read the data from the joystick file/device  ##
    #####################################################################

    while using_controller:
        # read 8 bits from the event buffer.
        event_buffer = jsdev.read(8)
        if event_buffer:
            time, value, type, number = struct.unpack('IhBB', event_buffer)

            #  Button pressed event
            if type & 0x01:
                ########################
                # D-Pad button pressed #
                ########################
                if (number >= 4) and (number <= 7):
                    dpad_button_pressed(
                        value, number, joystickD_padCurrentButton)

                    # only change current button when it is pressed not released
                    if value:
                        joystickD_padCurrentButton = number
                #########################
                # All buttons NOT D-pad #
                #########################

                # Select button
                elif number == 0:

                    if value:
                        button_select_pressed()
                    else:
                        button_select_released()

                     #  Right paddle button
                elif number == 1:
                    if value:
                        button_right_paddle()

                #  Left Paddle button
                elif number == 2:
                    if value:
                        button_left_paddle()

                #  Start Paddle button
                elif number == 3:
                    if value:
                        button_start_pressed()
                    else:
                        button_start_released()

                # L2 button
                elif number == 8:
                    if value:
                        button_L2_pressed()
                    else:
                        button_L2_released()

                     # R2 button
                elif number == 9:
                    if value:
                        button_R2_pressed()
                    else:
                        button_R1_released()

                # L1 button
                elif number == 10:
                    if value:
                        button_L1_pressed()
                    else:
                        button_L1_released()
                # R1 button
                elif number == 11:
                    if value:
                        button_R1_pressed()
                    else:
                        button_R1_released()

                # triangle button
                elif number == 12:
                    if value:
                        button_triangle_pressed()
                    else:
                        button_triangle_released()

                # circle button
                elif number == 13:
                    if value:
                        button_circle_pressed()
                    else:
                        button_circle_released()

                #  Cross button
                elif number == 15:
                    if value:
                        button_square_pressed()
                    else:
                        button_square_released()

                #  Cross button
                elif number == 14:
                    if value:
                        button_cross_pressed()
                    else:
                        button_cross_released()

                #  PS3  button
                elif number == 16:
                    if value:
                        button_PS3()

                else:
                    pass
                    # debug.print_to_all_devices("you pressed {}" .format(number))

            # Axis movement event
            elif type & 0x02:
                pass
                # debug.print_to_all_devices('number{}'.format(number))

                # Tank mode
                if tank_drive_on == True:
                    if number == 1:
                        leftPaddle = int(value / 327.67)
                        tank_drive(leftPaddle, rightPaddle)

                    elif number == 3:
                        # debug.print_to_all_devices("right side..")
                        rightPaddle = int(value / 327.67)
                        tank_drive(leftPaddle, rightPaddle)

    # we have finished so clean up
    jsdev.close()


def main():
    init()
    start()
    drive.cleanup()


if __name__ == "__main__":
    debug.debug_on = True

    debug.turn_debug_on()                  # use the debug and turn on output

    # Set the GPIO pins as numbering - Also set in drive.py
    GPIO.setmode(GPIO.BOARD)
    # Turn GPIO warnings off - CAN ALSO BE Set in drive.py
    GPIO.setwarnings(False)

    drive.init()               # Initialise the software to control the motors

    main()
