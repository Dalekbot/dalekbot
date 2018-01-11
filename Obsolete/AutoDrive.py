import time
import DalekV2DriveV2
import DalekMag
import RPi.GPIO as GPIO  # Import GPIO divers

GPIO.setwarnings(False)
DalekV2DriveV2.init()
speed = 50

heading = DalekMag.getMag()


def DalekTurn(degreesToTurn):
    startHeading = DalekMag.getMag()
    currentHeading = startHeading
    endDegrees = 0
    endHeading = 0
    rotations = 0
    rotationsDegrees = 0
    direction = 0  # spinright

    print("\n~~~~~~~~~~")
    print("Deg to Turn:{}" .format(degreesToTurn))

    # normalise the data a
    if degreesToTurn < 0:
        direction = 1
        degreesToTurn = -degreesToTurn

    # more than one rotation
    if degreesToTurn > 360:
        rotations = int(degreesToTurn / 360)
        rotationsDegrees = int(degreesToTurn % 360)
        print("Rotations:{} then Deg:{}" .format(rotations, rotationsDegrees))
    else:
        rotationsDegrees = degreesToTurn

    # start the turning
    # Clockwise
    if direction == 0:
        # calculate endHeading
        if (currentHeading + rotationsDegrees) > 360:
            endHeading = currentHeading + rotationsDegrees - 360
            print("C1")
        else:
            endHeading = currentHeading + rotationsDegrees
            print("C2")

        endDegrees = startHeading + degreesToTurn
        print("Clockwise:{}" .format(endDegrees))

        hasRolledOver = False

        while (rotations > 0) and
        # DalekV2DriveV2.spinRight(70)
    else:
        if (currentHeading - rotationsDegrees) < 0:
            endHeading = currentHeading - rotationsDegrees + 360
            print("AC1")
        else:
            endHeading = currentHeading - rotationsDegrees
            print("AC1")
        endDegrees = startHeading - degreesToTurn
        print("Anticlockwise:{}" .format(endDegrees))

    print("starting Turn-- Current:{} newHeadding{}".format(currentHeading, endHeading))
    print("~~~~~~~~~~\n")


print("\n\n-----------------------------------------------------------")
DalekTurn(-395)
DalekTurn(395)
DalekTurn(-25)
DalekTurn(90)
DalekTurn(190)


# DalekV2DriveV2.stop()
# newHeading = heading + 45
# print("starting Turn-- Current:{} New:{}".format(heading, newHeading))
# # time.sleep(2)

# DalekV2DriveV2.spinRight(70)
# while heading <= newHeading:


#     heading = DalekMag.getMag()
#     # time.sleep(.1)
#     # DalekV2DriveV2.stop()
#     # time.sleep(.1)
#     print("newHeading:{}" .format(newHeading))
#     # time.sleep(1)

# DalekV2DriveV2.stop()
# heading = DalekMag.getMag()
# print("Ended Turn-- Current:{} Should be:{}".format(heading, newHeading))
DalekV2DriveV2.cleanup()
