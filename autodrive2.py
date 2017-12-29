import time
import DalekV2DriveV2
import autoDrive
import DalekSpi
import RPi.GPIO as GPIO  # Import GPIO divers
from DalekDebug import DalekPrint, DalekDebugOn , DalekDebugSetOutputDevice

 
GPIO.setwarnings(False)
# DalekV2DriveV2.init()
DalekSpi.init()
DalekDebugOn()

# dalekSpeed = 40



# def driveForwardsToDistance(distance):
  
#   DalekPrint("driveForwards()")
#   dalekData = DalekSpi.readDevice1Data()
#   while dalekData['frontPing'] != distance:
   
#     dalekSpeed = autoDrive.CalculateSpeedToDrive(dalekData['frontPing'],distance)

#     if dalekData['frontPing'] <= distance:
      
#       DalekV2DriveV2.backward(dalekSpeed)


#     else:
      
#       DalekV2DriveV2.forward(dalekSpeed)
    
#     # time.sleep(.5)
#     dalekData = DalekSpi.readDevice1Data()
 
      

    

# def driveBackwardsToDistance(distance):
  
#   DalekPrint("driveBackwards()")
#   dalekData = DalekSpi.readDevice1Data()
  
#   while dalekData['rearPing'] != distance:
#     dalekSpeed = autoDrive.CalculateSpeedToDrive(dalekData['rearPing'],distance)
    

#     if dalekData['rearPing'] <= distance:
      
#       DalekV2DriveV2.forward(dalekSpeed)
#     else:
#       DalekV2DriveV2.backward(dalekSpeed)
    
#     # time.sleep(.1)
#     dalekData = DalekSpi.readDevice1Data()
 
    
  
head =90
# autoDrive.gotoHeading(108)

DalekPrint(autoDrive.getMag())
# time.sleep(.5)

autoDrive.gotoHeading(180)
autoDrive.gotoHeading(head)
autoDrive.driveForwardsToDistance(10)
autoDrive.DalekTurn(90)
autoDrive.DalekTurn(-90)
DalekPrint("Heading:{}".format(autoDrive.getMag()))
autoDrive.driveBackwardsToDistance(10)

DalekPrint("Heading:{}".format(autoDrive.getMag()))
# time.sleep(.5)
autoDrive.gotoHeading(head)
autoDrive.gotoHeading(180)
autoDrive.gotoHeading(head)
autoDrive.driveForwardsToDistance(10)
DalekPrint("Heading:{}".format(autoDrive.getMag()))
autoDrive.driveBackwardsToDistance(10)

DalekPrint("Heading:{}".format(autoDrive.getMag()))
# time.sleep(.5)
autoDrive.gotoHeading(head)
autoDrive.driveForwardsToDistance(10)
autoDrive.driveBackwardsToDistance(10)




autoDrive.dispose()