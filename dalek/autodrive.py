#!/usr/bin/env python
import time
import DalekV2Drive
import DalekSpi
import RPi.GPIO as GPIO  # Import GPIO divers

from DalekDebug import DalekPrint

GPIO.setwarnings(False)
DalekV2Drive.init()
DalekSpi.init()

# TODO # needs kill switch


# this is the default distance the bot drives to the wall.
DistanceToWall = 10


# all these settings can be altered  depending on the surface you are driving on
#-- sleepTime allows the bot to stop before a mag reading is taken
#     if you take a reading when the bot is moving, Acceleration and the motor's magnets will
#     have an effect on it, so we stop it and take a reading.
#-- TurnSpeeds can be increased until you notice the bot overshooting and needing
#     to go in the opposite direction to correct it's self.
#-- BotMoveTime is the time it moves at the TurnSpeed again check for overshooting

# Carpet settings
DalekTurnSettings = {
    'sleepTime': 0.4,
    'TurnSpeedFast': 70,
    'TurnSpeedNormal': 50,
    'TurnSpeedSlow': 40,
    'TurnSpeedFinal': 30,
    'BotMoveTimeFast': 1.0,
    'BotMoveTimeNormal': 0.6,
    'BotMoveTimeSlow': 0.4,
    'BotMoveTimeFinal': 0.2}


def changeDalekTurnSettings(number=None):
    # global DalekTurnSettings
    if number == None:
        # Carpet settings
        DalekTurnSettings = {
            'sleepTime': 0.4,
            'TurnSpeedFast': 70,
            'TurnSpeedNormal': 50,
            'TurnSpeedSlow': 40,
            'TurnSpeedFinal': 30,
            'BotMoveTimeFast': 1.0,
            'BotMoveTimeNormal': 0.6,
            'BotMoveTimeSlow': 0.4,
            'BotMoveTimeFinal': 0.2}
    elif number == 1:
        # Wooden floor settings
        DalekTurnSettings = {
            'sleepTime': 0.2,
            'TurnSpeedFast': 60,
            'TurnSpeedNormal': 40,
            'TurnSpeedSlow': 20,
            'TurnSpeedFinal': 30,
            'BotMoveTimeFast': .7,
            'BotMoveTimeNormal': 0.4,
            'BotMoveTimeSlow': 0.2,
            'BotMoveTimeFinal': 0.2}


def DalekTurn(degreesToTurn):

    def getMag():
        DalekV2Drive.stop()
        time.sleep(DalekTurnSettings['sleepTime'])
        currentMag = -1
        # ensure we get a valid reading must be between 0 and 360
        while not (0 <= currentMag <= 360):
            currentMag = DalekSpi.getMag()
        # print("---getStartingMag:{}".format(currentMag))
        return currentMag

    def calculateEndHeading(degreesToTurn):

        # we don't need more than one rotation.
        if degreesToTurn > 360:
            degreesToTurn = degreesToTurn % 360
        if degreesToTurn < -360:
            degreesToTurn = -degreesToTurn
            degreesToTurn = degreesToTurn % 360
            degreesToTurn = -degreesToTurn

        currentHeading = getMag()
        finalHeading = (currentHeading + degreesToTurn) % 360
        print("\n~~~~~~~~~~~~~~~~~\ndegreesToTurn:{}       currentMag:{}        FinalHeading:{}".format(
            degreesToTurn, currentHeading, finalHeading))
        return currentHeading, finalHeading

    # I am a robot I want the quickest route.
    def calculateTurnDirection(endHeading):
        turnClockwise = True
        turnSpeed = 60
        currentHeading = getMag()
        diffBetweenStartAndEnd = 0
        botMoveTime = 1

        if endHeading < currentHeading:
            print("less")
            diffBetweenStartAndEnd = -(currentHeading - endHeading)
            print("  diffBetweenStartAndEnd:{}   \n ".format(
                diffBetweenStartAndEnd))

            if (-180 <= diffBetweenStartAndEnd <= 180):
                print("this way")
                if (0 <= diffBetweenStartAndEnd <= 180):
                    print(">>>Turn Clockwise:{} deg".format(
                        diffBetweenStartAndEnd))
                    turnClockwise = True
                else:
                    print(
                        ">>>Turn anti Clockwise:{} deg".format(-diffBetweenStartAndEnd))
                    turnClockwise = False

            else:
                print("switch direction")
                var2 = 180 - ((currentHeading - endHeading) - 180)
                print("  diffBetweenStartAndEnd:{}   \n ".format(var2))

        else:
            print("more")
            diffBetweenStartAndEnd = endHeading - currentHeading
            print("@@@@@@  diffBetweenStartAndEnd:{}   \n ".format(
                diffBetweenStartAndEnd))
            if diffBetweenStartAndEnd > 180:
                ttt = diffBetweenStartAndEnd - 180
                print("<<<Turn anti Clock wise:{} deg".format(ttt))
                turnClockwise = False
            else:
                print("<<<Turn  Clock wise:{} deg".format(
                    diffBetweenStartAndEnd))
                turnClockwise = True
        if diffBetweenStartAndEnd < 0:
            diffBetweenStartAndEnd = -diffBetweenStartAndEnd

        if diffBetweenStartAndEnd >= 60:
            turnSpeed = DalekTurnSettings['TurnSpeedFast']
            botMoveTime = DalekTurnSettings['BotMoveTimeFast']
        elif 21 <= diffBetweenStartAndEnd <= 59:
            turnSpeed = DalekTurnSettings['TurnSpeedNormal']
            botMoveTime = DalekTurnSettings['BotMoveTimeNormal']
        elif 10 <= diffBetweenStartAndEnd <= 20:
            turnSpeed = DalekTurnSettings['TurnSpeedSlow']
            botMoveTime = DalekTurnSettings['BotMoveTimeSlow']

        else:  # diffBetweenStartAndEnd <= 20
            turnSpeed = DalekTurnSettings['TurnSpeedFinal']
            botMoveTime = DalekTurnSettings['BotMoveTimeFinal']

        return turnClockwise, turnSpeed, currentHeading, botMoveTime

    ##################################################################
    # initialise values
    # botTurnClockwise= True
    # botSpeed = 60
    # botCurrentHeading= -1
    # botMoveTime = 1
    # get end heading
    botCurrentHeading, finalHeading = calculateEndHeading(degreesToTurn)

    # set current values
    botTurnClockwise, botSpeed, botCurrentHeading, botMoveTime = calculateTurnDirection(
        finalHeading)
    # now do your stuff until you get to where you need to be.
    while botCurrentHeading != finalHeading:
        print("\n####################\ncurrentMag:{} ShouldBe:{} speed:{}".format(
            botCurrentHeading, finalHeading, botSpeed))

        if botTurnClockwise:
            DalekV2Drive.spinRight(botSpeed)
        else:
            DalekV2Drive.spinLeft(botSpeed)
        time.sleep(botMoveTime)
        # DalekV2Drive.stop()
        # time.sleep(.3)
        botTurnClockwise, botSpeed, botCurrentHeading, botMoveTime = calculateTurnDirection(
            finalHeading)

    DalekV2Drive.stop()
    time.sleep(.3)
    botCurrentHeading = getMag()
    print("\n--------------------\n  END \n    currentMag:{} ShouldBe:{} speed:{}".format(
        botCurrentHeading, finalHeading, botSpeed))


def printMag():
    DalekV2Drive.stop()
    time.sleep(DalekTurnSettings['sleepTime'])
    currentMag = -1
    # ensure we get a valid reading must be between 0 and 360
    while not (0 <= currentMag <= 360):
        currentMag = DalekSpi.getMag()

    print("---getStartingMag:{}".format(currentMag))
    return currentMag


def getMag():
    DalekV2Drive.stop()
    time.sleep(DalekTurnSettings['sleepTime'])
    currentMag = -1
    # ensure we get a valid reading must be between 0 and 360
    while not (0 <= currentMag <= 360):
        currentMag = DalekSpi.getMag()
    return currentMag


def gotoHeading(theEndHeading):
    theStartHeading = printMag()
    turn = 0
    if theStartHeading >= theEndHeading:
        turn = - (theStartHeading - theEndHeading)
    else:
        turn = theEndHeading - theStartHeading

    DalekTurn(turn)

    print("start {} end:{} change:{}".format(
        theStartHeading, theEndHeading, turn))

# use this if you get non liner readings from your mag
# you turn the bot when told and it gives you the readings you can use to drive it.


def calibrate():

    print("starting calibration process...")
    time.sleep(.5)

    print("position in start direction.")
    time.sleep(5)
    m1 = getMag()
    print("-{}".format(m1))
    time.sleep(.5)
    m2 = getMag()
    print("--{}".format(m2))
    time.sleep(.5)
    m3 = getMag()
    print("---{}".format(m3))
    d1 = int((m1 + m2 + m3) / 3)
    print("Start Position:{}".format(d1))
    time.sleep(.5)

    print("Turn bot 90 deg Clockwise.")
    time.sleep(5)
    m1 = getMag()
    print("-{}".format(m1))
    time.sleep(.5)
    m2 = getMag()
    print("--{}".format(m2))
    time.sleep(.5)
    m3 = getMag()
    print("---{}".format(m3))
    d2 = int((m1 + m2 + m3) / 3)

    print("Turn bot 90 deg Clockwise.")
    time.sleep(5)
    m1 = getMag()
    print("-{}".format(m1))
    time.sleep(.5)
    m2 = getMag()
    print("--{}".format(m2))
    time.sleep(.5)
    m3 = getMag()
    print("---{}".format(m3))
    d3 = int((m1 + m2 + m3) / 3)

    print("Turn bot 90 deg Clockwise.")
    time.sleep(5)
    m1 = getMag()
    print("-{}".format(m1))
    time.sleep(.5)
    m2 = getMag()
    print("--{}".format(m2))
    time.sleep(.5)
    m3 = getMag()
    print("---{}".format(m3))
    d4 = int((m1 + m2 + m3) / 3)

    print("calibration Finished {},{},{},{}".format(d1, d2, d3, d4))

    return d1, d2, d3, d4


def calibrateAndTest():
    d1, d2, d3, d4 = calibrate()
    gotoHeading(d1)
    gotoHeading(d2)
    gotoHeading(d3)
    gotoHeading(d4)
    gotoHeading(d2)


##########################################################
#          PING SENSOR FUNCTIONS
##########################################################

# TODO add mode for different surfaces if needed

# this slows down the bot as it gets closer to an object
def CalculateSpeedToDrive(pingDistance, finalDistance):
    howClose = pingDistance - finalDistance
    dalekSpeed = 0
    if howClose > 41:
        dalekSpeed = 35
    elif howClose > 21:
        dalekSpeed = 30
    elif howClose > 12:
        dalekSpeed = 20
    elif howClose > 6:
        dalekSpeed = 14
    else:
        dalekSpeed = 11
    return dalekSpeed


# This uses the front ultrasonic sensor.
def driveForwardsToDistance(distance):

    DalekPrint("driveForwards()")
    dalekData = DalekSpi.readDevice1Data()
    DalekPrint(dalekData)
    while dalekData['frontPing'] != distance:

        dalekSpeed = CalculateSpeedToDrive(dalekData['frontPing'], distance)

        if dalekData['frontPing'] <= distance:
            DalekV2Drive.backward(dalekSpeed)
        else:
            DalekV2Drive.forward(dalekSpeed)
        dalekData = DalekSpi.readDevice1Data()

# this uses the Rear ultrasonic sensor.


def driveBackwardsToDistance(distance):

    DalekPrint("driveBackwards()")
    dalekData = DalekSpi.readDevice1Data()

    while dalekData['rearPing'] != distance:
        dalekSpeed = CalculateSpeedToDrive(dalekData['rearPing'], distance)

        if dalekData['rearPing'] <= distance:
            DalekV2Drive.forward(dalekSpeed)
        else:
            DalekV2Drive.backward(dalekSpeed)
        dalekData = DalekSpi.readDevice1Data()

# drive parallel  to wall and if we are not within
# the tolerance given we make the corrections.
# when the wall disaperes we conclude it is time for the
# next waypoint


def driveParallelToLeftWall(distanceToWall=None):
    DalekPrint("driveParallelToLeftWall()")
    dalekData = DalekSpi.readDevice1Data()
    if distanceToWall == None:
        distanceToWall = DistanceToWall

    initialSensorData = DalekSpi.readDevice1Data()
    DalekPrint("initialSensorData:{}".format(initialSensorData))

    if initialSensorData['leftPing'] >= distanceToWall:
        pass


def driveParallelToRightWall(distanceToWall):
    pass


def driveParallelToWallsInCenterToFrontPingDistance(distanceToWall=None):
    pass


def dispose():
    DalekV2Drive.cleanup()


# TEST
# DalekTurn(-361)
# DalekTurn(360449)
# while True:
#   printMag()
#   time.sleep(2)


# d1 = 290
# d2 = 26
# d3 = 96
# d4 = 160


# gotoHeading(d3)
# gotoHeading(d4)
# gotoHeading(d1)


# printMag()
# time.sleep(2)

# DalekTurn(154)
# DalekV2Drive.stop()
# DalekTurn(-154)
# DalekTurn(355)
# DalekTurn(90)
# DalekTurn(-400)
# DalekTurn(-90)
# DalekTurn(-180)
# DalekTurn(180)
# DalekTurn(-181)
# DalekTurn(-359)
# DalekTurn(280)
# time.sleep(.3)
# DalekV2Drive.stop()
# printMag()
