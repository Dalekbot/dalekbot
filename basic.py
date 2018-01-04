from DalekDebug import DalekPrint, DalekDebugOn , DalekDebugSetOutputDevice
import time
import DalekSpi
import RPi.GPIO as GPIO  # Import GPIO divers
DalekSpi.init()

DalekDebugOn()
DalekPrint("hello phil from the main module")

while True:
  global SpiSetup,spi
  # piSensors = DalekSpi.readDevice1Data() 
  # DalekPrint(piSensors['frontPing'] )
  # DalekPrint(piSensors['compass'] )

  mag = DalekSpi.getSensorData(4)
  DalekPrint(mag)
  time.sleep(1)

 

