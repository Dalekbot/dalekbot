from DalekDebug import DalekPrint, DalekDebugOn , DalekDebugSetOutputDevice, DalekDebugClear
import time
import DalekSpi
import RPi.GPIO as GPIO  # Import GPIO divers
DalekSpi.init()


#####################################################

#     This is for end to end Tests 
#     This file should run on any bot it is put on

#####################################################

# nothing should printOut
DalekPrint("Bang!!")
DalekPrint("Pop", "POP")
DalekPrint("Hiss","PSS")


DalekDebugOn()
# print some stuff out with no onboard display
DalekPrint("Spin Left 56","SL")
DalekPrint("Spin Left {}".format(666),"KKK" )
DalekPrint("Turn Right 56")
DalekPrint("... Shutting Down...")
DalekPrint("Returning to Main Menu", "HM")
DalekPrint("","PSS")

# now use the scrollphat
DalekDebugSetOutputDevice("scrollphat")
DalekPrint("TURNING ON BOTS DISPLAY","ON")
time.sleep(1)

DalekPrint("TURNING OFF BOTS DISPLAY","  ")
DalekDebugClear(.5)
DalekPrint("1","888")
DalekDebugClear(.5)
DalekPrint("2","888")
DalekDebugClear(.5)
DalekPrint("Done!","888")
DalekDebugClear()
