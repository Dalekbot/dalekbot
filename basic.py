from dalek_debug import DalekPrint, DalekDebugOn , DalekDebugSetOutputDevice
import time
import dalek_spi
import RPi.GPIO as GPIO  # Import GPIO divers
dalek_spi.init()


#####################################################

#     This is just for playing with the bits to see if it works :)
#     do not leave code here that you need 

#####################################################
DalekDebugOn()
# DalekDebugSetOutputDevice("scrollphat")
# DalekPrint("hello phil from the main module")

DalekPrint("Spin Left 56","SL")
DalekPrint("Spin Left {}".format(666),"KKK" )
DalekPrint("Turn Right 56")
DalekPrint("\n... Shutting Down...\n")
DalekPrint("\n\nReturning to Main Menu\n\n", "HM")
DalekPrint("","PSS")
# while True:
  
#   # piSensors = DalekSpi.readDevice1Data() 
#   # DalekPrint(piSensors['frontPing'] )
#   # DalekPrint(piSensors['compass'] )
#   DalekSpi.test()

#   # mag = DalekSpi.readDevice1Data()
#   # DalekPrint(mag)
#   time.sleep(.2)

 
