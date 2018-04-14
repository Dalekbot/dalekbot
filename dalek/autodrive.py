if __name__ == "__main__":
    '''
    This if statement is needed for testing, to locate the modules needed
    if we are running the file directly.
    '''
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    import RPi.GPIO as GPIO  # Import GPIO divers

    GPIO.setwarnings(False)


#!/usr/bin/env python3
import time
from dalek import spi
from dalek import drive
from dalek import debug
from dalek import head_controller

drive.init()

# this is the default distance the bot drives to the wall.
distance_to_wall = 15

compass_positions = {'forward': -1, 'right': -1, 'left': -1, 'backwards': -1}
# start the sensor service.
DalekSensors = spi.SensorData()
DalekSensors.start()


# all these settings can be altered  depending on the surface you are driving on
#-- sleepTime allows the bot to stop before a mag reading is taken
#     if you take a reading when the bot is moving, Acceleration and the motor's magnets will
#     have an effect on it, so we stop it and take a reading.
#-- TurnSpeeds can be increased until you notice the bot overshooting and needing
#     to go in the opposite direction to correct it's self.
#-- BotMoveTime is the time it moves at the TurnSpeed again check for overshooting

# Carpet settings
# DalekTurnSettings = {
#     'sleepTime': 0.4,
#     'TurnSpeedFast': 80,
#     'TurnSpeedNormal': 60,
#     'TurnSpeedSlow': 60,
#     'TurnSpeedFinal': 60,
#     'BotMoveTimeFast': 0.8,
#     'BotMoveTimeNormal': 0.4,
#     'BotMoveTimeSlow': 0.5,
#     'BotMoveTimeFinal': 0.5}


# def changeDalekTurnSettings(number=None):
#     # global DalekTurnSettings
#     if number == None:
#         # Carpet settings
#         DalekTurnSettings = {
#             'sleepTime': 0.4,
#             'TurnSpeedFast': 70,
#             'TurnSpeedNormal': 50,
#             'TurnSpeedSlow': 40,
#             'TurnSpeedFinal': 30,
#             'BotMoveTimeFast': 1.0,
#             'BotMoveTimeNormal': 0.6,
#             'BotMoveTimeSlow': 0.4,
#             'BotMoveTimeFinal': 0.2}
#     elif number == 1:
#         # Wooden floor settings
#         DalekTurnSettings = {
#             'sleepTime': 0.2,
#             'TurnSpeedFast': 60,
#             'TurnSpeedNormal': 40,
#             'TurnSpeedSlow': 20,
#             'TurnSpeedFinal': 30,
#             'BotMoveTimeFast': .7,
#             'BotMoveTimeNormal': 0.4,
#             'BotMoveTimeSlow': 0.2,
#             'BotMoveTimeFinal': 0.2}


# sensor distance will get bigger then 
# get smaller again, this is the point you need to find
# it will then get larger again

def turn_right_90_deg_with_sonic():
    turnspeed = 50

    
    while True :
        distance = DalekSensors.left_distance
        print("{}".format(distance))
        drive.spinRight(turnspeed)
        if distance> 30:
            break


def turn_right_90_deg():
    turnspeed = 50
    ## start 162 end 42
    
    ##' take new compass readings
    head_controller.head_move_to_center(0)
    time.sleep(.4)
    compass_positions['forward'] = DalekSensors.compass

    head_controller.head_move_right_90deg(0)
    time.sleep(.8)
    compass_positions['right'] = DalekSensors.compass

    print("{} goto -> {}".format(compass_positions['forward'],compass_positions['right']))
    head_controller.head_move_to_center(0)
    time.sleep(.5)
    # go_past_360 = False


    # if we need to go past 360 point 
    if compass_positions['forward'] > compass_positions['right']:
        ## while between values to get past 360
        while compass_positions['forward'] <= DalekSensors.compass <= 360:
            drive.spinRight(turnspeed)
           # time.sleep(.2)
    
    
    while DalekSensors.compass < compass_positions['right']:
        drive.spinRight(turnspeed)
        #time.sleep(.2)
    # time.sleep(1)
    # while DalekSensors.compass < compass_positions['right']:
    #     drive.spinRight(turnspeed)
    #     time.sleep(.2)
        
    print(DalekSensors.compass)
    drive.stop()
    print("Stop")
    time.sleep(1)
    print(DalekSensors.compass)
    
   


    # todo flip all compass values to make forwards forward again
    
def gotoHeading(theEndHeading):
    pass

# use this if you get non liner readings from your mag
# you turn the bot when told and it gives you the readings you can use to drive it.


def calibrate_compass():
    head_controller.leds_change_color(head_controller.leds_color['yellow'])
    print("point your bot in the forward position.")
    time.sleep(3)
    head_controller.head_move_to_center()
    time.sleep(1)
    compass_positions['forward'] = DalekSensors.compass
    print("center mag:{}" .format(compass_positions['forward']))

    head_controller.head_move_left_90deg()
    time.sleep(2)
    compass_positions['left'] = DalekSensors.compass
    print("left mag:{}" .format(compass_positions['left']))

    head_controller.head_move_right_90deg()
    time.sleep(2)
    compass_positions['right'] = DalekSensors.compass
    print("right mag:{}" .format(compass_positions['right']))

    head_controller.head_move_to_center()
    time.sleep(2)
    head_controller.leds_change_color(head_controller.leds_color['off'])

    # TODO: turn dalek and get backwards...


##########################################################
#          PING SENSOR FUNCTIONS
##########################################################

# TODO add mode for different surfaces if needed

# this slows down the bot as it gets closer to an object
def CalculateSpeedToDrive(pingDistance, finalDistance):
    howClose = pingDistance - finalDistance
    dalekSpeed = 0
    if howClose > 41:
        dalekSpeed = 60
    elif howClose > 21:
        dalekSpeed = 50
    elif howClose > 12:
        dalekSpeed = 40
    elif howClose > 6:
        dalekSpeed = 30
    else:
        dalekSpeed = 20
    return dalekSpeed


# This uses the front faceing sensor.
def drive_forwards_to_distance(distance=distance_to_wall):
    # counter =0
    print("drive_forwards_to_distance()")

    
    while DalekSensors.front_distance != distance:
        
        ## get the speed to drive at
        speed = CalculateSpeedToDrive( DalekSensors.front_distance, distance)

        if DalekSensors.front_distance <= distance:
            drive.backward(speed)
            print("drive_backwards()")
        else:
            # l_speed = speed
            # r_speed = speed
            # if(DalekSensors.left_distance > 13):

            #     l_speed -= 10
            #     # r_speed +=10
            #     print("LS {}".format(DalekSensors.left_distance))
            # elif ( DalekSensors.left_distance < 9):
            #     r_speed -= 10
            #     l_speed += 10 
            #     print("RS {}".format(DalekSensors.left_distance))
            # drive.paddleForward(l_speed,r_speed) 
            drive.paddleForward(speed,speed)
    drive.stop()
    straighten_up() 


 
        # counter+=1
    # print("counter:{}".format(counter))
def straighten_up():
    print("{} {} {}".format(DalekSensors.laser_front_left,DalekSensors.front_distance, DalekSensors.laser_front_right))
    
    lz_left = DalekSensors.laser_front_left
    lz_right = DalekSensors.laser_front_right
    while lz_left != lz_right :
        if lz_left > lz_right:
            drive.spinRight(30)
        elif lz_left < lz_right:
            drive.spinLeft(30) 
        time.sleep(.1)
        print("{} {} ".format(lz_left,lz_right))
  
        lz_left = DalekSensors.laser_front_left 
        lz_right = DalekSensors.laser_front_right

    print("{} {} ".format(lz_left,lz_right))
    drive.stop()
# this uses the Rear ultrasonic sensor.


def drive_backwards_to_distance(distance=distance_to_wall):

    print("driveBackwards()")

    while DalekSensors.rear_distance != distance:
        dalekSpeed = CalculateSpeedToDrive(DalekSensors.rear_distance, distance)

        if DalekSensors.rear_distance <= distance:
            drive.forward(dalekSpeed)
        else:
            
            drive.backward(dalekSpeed)
    drive.stop()

# drive parallel  to wall and if we are not within
# the tolerance given we make the corrections.
# when the wall disaperes we conclude it is time for the
# next waypoint


def driveParallelToLeftWall(distanceToWall=None):
    pass
    # DalekPrint("driveParallelToLeftWall()")
    # dalekData = spi.readDevice1Data()
    # if distanceToWall == None:
    #     distanceToWall = DistanceToWall

    # initialSensorData = spi.readDevice1Data()
    # DalekPrint("initialSensorData:{}".format(initialSensorData))

    # if initialSensorData['leftPing'] >= distanceToWall:
    #     pass


def driveParallelToRightWall(distanceToWall):
    pass


def driveParallelToWallsInCenterToFrontPingDistance(distanceToWall=None):
    pass


def dispose():
    drive.cleanup()
  

def main():
    # print_compass()

    # head_controller.leds_change_color(head_controller.leds_color['yellow'])

    # head_controller.head_rotate(93,1)
    # time.sleep(4)
    # head_controller.head_rotate(16,0)
    # time.sleep(.5)
    # print(DalekSensors.compass)
    # head_controller.head_rotate(170,0)
    # time.sleep(.8)
    # print(DalekSensors.compass)
    # head_controller.head_rotate(93,0) 
    # time.sleep(.5)
    # print(DalekSensors.compass)
    # head_controller.leds_change_color(head_controller.leds_color['off'])
    time.sleep(1)
    turn_right_90_deg_with_sonic()
    # drive_backwards_to_distance()
    # drive_forwards_to_distance(15)
    # straighten_up()
    # drive_forwards_to_distance(10)
    # calibrate_compass()
    # turn_right_90_deg() 
    
    # time.sleep(1)
    # drive_forwards_to_distance(15)
    # straighten_up()
    # drive_forwards_to_distance(10)
    # # calibrate_compass()
    # turn_right_90_deg() 

    # time.sleep(1)
    # drive_forwards_to_distance(15)
    # straighten_up()
    # drive_forwards_to_distance(10)
    # # calibrate_compass()
    # turn_right_90_deg() 

    # time.sleep(1)
    # drive_forwards_to_distance(15)
    # straighten_up()
    # drive_forwards_to_distance(10)
    # # calibrate_compass()
    # turn_right_90_deg() 
 

def print_compass():
    print("L F R Rear {} {} {} {}".format(
        compass_positions['left'],
        compass_positions['forward'],
        compass_positions['right'],
        compass_positions['backwards']))

    
    # # changeDalekTurnSettings(1)
    # head_controller.leds_change_color(head_controller.leds_color['red'])
    # head_controller.head_move_to_center()
    # fw_mag = spi.get_mag()
    # print("center mag:{}" .format(fw_mag))

    # time.sleep(1)
    # print("3")
    # head_controller.head_move_left_90deg()
    # time.sleep(2)
    # left_mag = spi.get_mag()
    # print("left mag:{}" .format(left_mag))
    # time.sleep(.5)

    # # head_controller.head_move_right_90deg()
    # # time.sleep(2)
    # # right_mag = spi.get_mag()
    # # print("left mag:{}" .format(right_mag))
    # head_controller.head_move_to_center()
    # time.sleep(1)
    # # head_controller.leds_change_color(head_controller.leds_color['white'])
    # # DalekTurn(176)
    # # DalekTurn(354)
    # turnspeed = 60
    # print("mag:{}" .format(spi.get_mag()))
    # drive.spinLeft(turnspeed)
    # print(turnspeed)
    # time.sleep(1)
    # drive.spinLeft(turnspeed-20)
    # print(turnspeed-20)
    # time.sleep(1)
    # print("mag:{}" .format(spi.get_mag()))

    # turn_left()


def turn_left():
    turnspeed = 50
    while DalekSensors.compass > (145+5):
        drive.spinLeft(turnspeed)
        time.sleep(.2)

    print(DalekSensors.compass)
    drive.stop()
    print("Stop")
    time.sleep(1)
    print(DalekSensors.compass)
    DalekSensors.stop_running()


if __name__ == "__main__":

    main()
    drive.stop()
    head_controller.leds_change_color(head_controller.leds_color['off'])
    drive.cleanup()
    DalekSensors.stop_running()
