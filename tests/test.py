import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import time
# from  dalek import spi 
from dalek import debug
import RPi.GPIO as GPIO  # Import GPIO divers
# spi.init()


#####################################################

#     This is for end to end Tests 
#     This file should run on any bot it is put on

#####################################################

# nothing should printOut
debug.print_to_all_devices("Bang!!")
debug.print_to_all_devices("Pop", "POP")
debug.print_to_all_devices("Hiss","PSS")


DalekDebugOn()
# print some stuff out with no onboard display
debug.print_to_all_devices("Spin Left 56","SL")
debug.print_to_all_devices("Spin Left {}".format(666),"KKK" )
debug.print_to_all_devices("Turn Right 56")
debug.print_to_all_devices("... Shutting Down...")
debug.print_to_all_devices("Returning to Main Menu", "HM")
debug.print_to_all_devices("","PSS")

# now use the scrollphat
DalekDebugSetOutputDevice("scrollphat")
debug.print_to_all_devices("TURNING ON BOTS DISPLAY","ON")
time.sleep(1)

debug.print_to_all_devices("TURNING OFF BOTS DISPLAY","  ")
DalekDebugClear(.5)
debug.print_to_all_devices("1","888")
DalekDebugClear(.5)
debug.print_to_all_devices("2","888")
DalekDebugClear(.5)
debug.print_to_all_devices("Done!","888")
DalekDebugClear()
