#!/usr/bin/env python3
from dalek import scrollphat
import time

##################################################################
# This is an abstraction layer for our debuging                  #
# You can use the bash output window or plugin your own device.  #
##################################################################


debug_on = False
output_device = 0


def set_output_device(_dalekDebugOutputDevice):
    """ 
    sets the output device 
    default is stout/command line only
    "scollphat" adds the bots display as well as stout
    """
    global output_device

    if _dalekDebugOutputDevice == "scrollphat":

        scrollphat.clear()
        scrollphat.write_string("BOT")
        output_device = 1
        debug_on = True  # assume that as it is set,  use it.
    else:
        output_device = 0


def turn_debug_on():
    global debug_on
    debug_on = True


def turn_debug_off():
    global debug_on
    debug_on = False
# the text is the main bash output
# the code is the output to the bots screen


def print_to_all_devices(text, code=None):

    if debug_on:
        if output_device == 0:
            print(text)
        elif output_device == 1:
            # scrollphat
            print(text)
            if code != None:
                scrollphat.clear()
                scrollphat.write_string(code)
            pass


def clear(timeToPause=None):
    if output_device == 1:  # using the scrollphat
        scrollphat.clear()
    if timeToPause != None:
        time.sleep(timeToPause)


def set_brightness(valueInt):
    if output_device == 1:  # using the scrollphat
        scrollphat.set_brightness(valueInt)


def destroy():
    clear()


if __name__ == "__main__":
    print("\n\ndalek.debug.py cannot be run directly. It is intended to be imported\n\n")
else:
   pass # print("Importing dalek.debug.py")
