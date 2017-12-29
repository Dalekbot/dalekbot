from DalekDebug import DalekPrint, DalekDebugOn , DalekDebugSetOutputDevice
import time
import DalekSpi

DalekSpi.init()

DalekDebugOn()
DalekPrint("hello phil from the main module")

while True:
  DalekPrint(DalekSpi.readDevice1Data())
  time.sleep(.3)

 

