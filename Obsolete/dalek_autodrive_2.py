import time
# import DalekV2DriveV2
import autoDrive
# import DalekSpi
# import RPi.GPIO as GPIO  # Import GPIO divers
from DalekDebug import DalekPrint, DalekDebugOn , DalekDebugSetOutputDevice

 
# GPIO.setwarnings(False)
# DalekV2DriveV2.init()
# DalekSpi.init()
DalekDebugOn()
autoDrive.changeDalekTurnSettings() ## 1 for wooden floor
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

#  MIMIMAL MAZE
# __________________________________   7 stop    
# |                                 |         |
# |      1                    2     |         |
# |                                 |         |
# |           __________            |         |
# |          /                      |         |
# |         /     4         3       |         |
# |         |                      /          |
# |         |            _________/           |
# |         |                                 |
# |         |     5                      6    |    
# |         |                                 |   
# |         |_________________________________| 
    
#  MIMIMAL MAZE drive
 
# # goto waypoint one
# autoDrive.driveParallelToWallsInCenterToFrontPingDistance()
# autoDrive.DalekTurn(90)

# # goto waypoint two
# autoDrive.driveParallelToLeftWall()
# #  check for clearing of wall to right and save frontPing distance. 
# #  you should know when you are in the right place to turn
# autoDrive.DalekTurn(90)

# # goto waypoint three
# autoDrive.driveForwardsToDistance(10)
# autoDrive.DalekTurn(90)

# # goto waypoint four
# #  the wall in front might give false reading as its at 45deg
# #  unless you are down enough. so measure the left 
# #  and right wall distances to make sure. 
# autoDrive.driveForwardsToDistance(10)
# autoDrive.DalekTurn(-90)

# # goto waypoint five
# autoDrive.driveForwardsToDistance(10)
# autoDrive.DalekTurn(-90)

# # goto waypoint six 
# autoDrive.driveParallelToWallsInCenterToFrontPingDistance()


# # goto waypoint seven
# # this needs to be in autoDrivedriveParallelToWallsInCenterToFrontPingDistance()
# # check if both left and right walls have disappeared. 




## old test code

# head =90
# # autoDrive.gotoHeading(108)

# DalekPrint(autoDrive.getMag())
# # time.sleep(.5)

# autoDrive.gotoHeading(180)
# autoDrive.gotoHeading(head)
# autoDrive.driveForwardsToDistance(10)
# autoDrive.DalekTurn(90)
# autoDrive.DalekTurn(-90)
# DalekPrint("Heading:{}".format(autoDrive.getMag()))
# while True:   
  # autoDrive.gotoHeading(94)
  # autoDrive.driveBackwardsToDistance(10)
  
autoDrive.driveParallelToLeftWall(10)

  # autoDrive.DalekTurn(180)
# DalekPrint("Heading:{}".format(autoDrive.getMag()))
# # time.sleep(.5)
# autoDrive.gotoHeading(head)
# autoDrive.gotoHeading(head)
# autoDrive.driveForwardsToDistance(10)
# DalekPrint("Heading:{}".format(autoDrive.getMag()))
# autoDrive.driveBackwardsToDistance(10)

# DalekPrint("Heading:{}".format(autoDrive.getMag()))
# # time.sleep(.5)
# autoDrive.gotoHeading(head)
# autoDrive.driveForwardsToDistance(10)
# autoDrive.driveBackwardsToDistance(10)







autoDrive.dispose()