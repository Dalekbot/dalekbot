import time
import DalekV2DriveV2
import simpletest  # this uses the  adafruit driver.
# import DalekMag as simpletest
import RPi.GPIO as GPIO  # Import GPIO divers

GPIO.setwarnings(False)
DalekV2DriveV2.init()
speed = 50

heading = simpletest.getMag()


def DalekTurn(degreesToTurn):
    print("\n---------")
    print("DalekTurn({})".format(degreesToTurn))
    startHeading = simpletest.getMag()
    currentHeading = startHeading
    endHeading = 0
    rotationsFull = 0
    rotationDegrees = 0
    direction = 0

    # normalise the data a
    if degreesToTurn < 0:
        direction = 1  # 0 clockwise , 1 anticlockwise
        degreesToTurn = -degreesToTurn

     # Calculate if more than one rotation
    if degreesToTurn > 360:
        rotationsFull = int(degreesToTurn / 360)
        rotationDegrees = int(degreesToTurn % 360)
    else:
        rotationDegrees = degreesToTurn

    print("  Rotations:{} then Deg:{}  "    .format(
        rotationsFull, rotationDegrees))

    # Clockwise rotation
    if direction == 0:

        # check if it goes past 360
        if (startHeading + rotationDegrees) > 360:
            endHeading = startHeading + rotationDegrees - 360
            rotationsFull += 1
            print(" Rolls over 360")
            print("  currrent:{}  :{} Rotation then Deg:{} endheading:{}" .format(
                currentHeading, rotationsFull, rotationDegrees, endHeading))

        else:
            endHeading = startHeading + rotationDegrees
            print("  currrent:{}  :{} Rotation then Deg:{} endheading:{}" .format(
                currentHeading, rotationsFull, rotationDegrees, endHeading))
            print("  clockwise rotation")
        lastHeading = currentHeading

        # while (currentHeading -5 ) <=
        #  endHeading <= (currentHeading +5): # between 5 either side
        DalekV2DriveV2.spinRight(speed)
        while (endHeading >= currentHeading)  :  # between 5 either side
            DalekV2DriveV2.spinRight(speed)
            print("  speed:{}".format(speed))
            time.sleep(.2)
           
            currentHeading = simpletest.getMag()
            print("  currrent:{}  :{} Rotation then Deg:{} endheading:{}" .format(
                currentHeading, rotationsFull, rotationDegrees, endHeading))
            lastHeading = currentHeading

            # if currentHeading <= (lastHeading):  # gone past the 360 point
                # rotationsFull -= 1
                

        print("done currentHeading:{}".format(currentHeading))
        DalekV2DriveV2.stop()

    # anticlockwise rotation
    else:
        print("  anticlockwise rotation")


# print("\n\n-----------------------------------------------------------")
# print("start deg:{}".format(simpletest.getMag()))
# print( simpletest.getMag())
# print( simpletest.getMag())
# print( simpletest.getMag())
# print( simpletest.getMag())
# print( simpletest.getMag())
# DalekTurn(-395)
# DalekTurn(45)


# while True:
#   print( simpletest.getMag())
#   time.sleep(.5)
# DalekV2DriveV2.cleanup()
 #  __main__ Code
#======================================================================	   
    
if __name__ == "__main__":
    print("\n\nThis file cannot be run directly. It is intended to be imported\n\n")
else:
    print("\n\nImporting autoDrive2.py")
    
# End of __main__ Code
#======================================================================