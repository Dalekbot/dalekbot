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



def turn_right_90_deg_with_sonic():
    turnspeed = 50

    
    while True :
        distance = DalekSensors.left_distance
        print("{}".format(distance))
        drive.spinRight(turnspeed)
        if distance> 30:
            break
def calculate_degrees_still_to_turn(start_degrees,end_degrees,direction_clockwise=True):
    current_compass = DalekSensors.compass
    
    if direction_clockwise:
        while 0 < current_compass > 360:
            current_compass = DalekSensors.compass
        # we have over shot
        if ((current_compass > end_degrees) and(current_compass < end_degrees+20)):
            return end_degrees - current_compass # should be negative number
        # we need to pass 360 
        elif current_compass > end_degrees:
            return 360 - current_compass + end_degrees
        else:#current_compass >= end:
            return end_degrees - current_compass
    else: # anticlockwise
        pass





def get_compass_turn_right_90_deg(saved_position = -1):
    turnspeed = 40 
    # take current reading
    head_controller.head_move_to_center(0)
    time.sleep(.4)
    c_f=DalekSensors.compass
    c_r=-1
    # we can use previous values from calibrated or previous runs.
    # this will save a few seconds
    if saved_position == -1:
        # take reading right
        head_controller.head_move_right_90deg(0)
        time.sleep(.8)
        c_r= DalekSensors.compass
    else: 
        c_r = saved_position
    # reset head
    head_controller.head_move_to_center(0)
    # time.sleep(.4)
    print("{} {}" .format(c_f,c_r))
    
    deg_to_turn = calculate_degrees_still_to_turn(c_f,c_r,True)
    print(deg_to_turn)
    # use the between syntax
    while -20 < deg_to_turn > 20:
        print("#### FAST #####")
        
        if deg_to_turn >0:
            drive.spinRight(turnspeed)
        elif deg_to_turn < -1:
            print("spinLeft")
            drive.spinLeft(turnspeed)
        deg_to_turn = calculate_degrees_still_to_turn(c_f,c_r,True)
    
    #repeat but slower to get it spot on
    while -1 < deg_to_turn > 1:
        print("#### SLOW #####")
        if deg_to_turn >0:
            drive.spinRight(turnspeed-10)
        elif deg_to_turn < -1:
            print("spinLeft")
            drive.spinLeft(turnspeed-10)
        deg_to_turn = calculate_degrees_still_to_turn(c_f,c_r,True)
       
    drive.stop()
    print("END {} {} {}" .format(c_f,c_r,DalekSensors.compass))
 

   


def turn_right_90_deg():
    turnspeed = 40 
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
        print("---Past 360")
        time.sleep(1)
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
    

def gotoHeading(theEndHeading):
    pass

# use this if you get non liner readings from your mag
# you turn the bot when told and it gives you the readings you can use to drive it.


def calibrate_compass():
    head_controller.leds_change_color(head_controller.leds_color['yellow'])
    print("point your bot in the forward position.")
    head_controller.head_move_to_center()
    time.sleep(3)
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
    head_controller.leds_change_color(head_controller.leds_color['green'])

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
            drive.paddleForward(speed,speed)
    drive.stop()


 
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
  
def turn_right_90_deg_left_laser():
    lz_left = DalekSensors.laser_front_left
    lz_center = DalekSensors.front_distance
    lz_right= DalekSensors.laser_front_right

    print("{} {} {}" .format(lz_left ,lz_center, lz_right))

    while DalekSensors.front_distance < 80:
        drive.spinRight(40)


    while (lz_left < 40 ) :
        lz_left = DalekSensors.laser_front_left
        lz_center = DalekSensors.front_distance
        lz_right= DalekSensors.laser_front_right
        print("{} {} {}" .format(lz_left ,lz_center, lz_right))
        drive.spinRight(40)

def turn_left_90_deg_right_laser():
    lz_left = DalekSensors.laser_front_left
    lz_center = DalekSensors.front_distance
    lz_right= DalekSensors.laser_front_right

    print("{} {} {}" .format(lz_left ,lz_center, lz_right))

    while DalekSensors.front_distance < 80:
        drive.spinLeft(40)


    while (lz_right < 50 ) :
        lz_left = DalekSensors.laser_front_left
        lz_center = DalekSensors.front_distance
        lz_right= DalekSensors.laser_front_right
        print("{} {} {}" .format(lz_left ,lz_center, lz_right))
        drive.spinLeft(40)

    
        

    drive.stop()
def turn_2():
    turn_right_90_deg()
    # start_mag = DalekSensors.compass
    # head_controller.head_move_right_90deg()
    # time.sleep(1)
    # dest_mag = DalekSensors.compass
    # print("{} {}".format(start_mag,dest_mag))
    # time.sleep(.5)
    # while 
    # head_controller.head_move_to_center()
    # drive.stop() 

         
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
    # head_controller.head_move_to_center()
    # time.sleep(1)
    get_compass_turn_right_90_deg()
    get_compass_turn_right_90_deg()
    get_compass_turn_right_90_deg()
    get_compass_turn_right_90_deg()
    # get_compass_turn_right_90_deg()
    # turn_right_90_deg_with_sonic()
    # drive_backwards_to_distance()
    # drive_forwards_to_distance(15)
    # straighten_up()
    # calibrate_compass()

    # waypoint 1
    # drive_forwards_to_distance(9)
    # turn_right_90_deg_left_laser() 
    
    # waypoint 2
    # drive_forwards_to_distance(45)
    # get_compass_turn_right_90_deg()
   # waypoint 3
    # drive_forwards_to_distance(8)
    # straighten_up()
    # get_compass_turn_right_90_deg()
    
    # HALFWAY
    # waypoint 4
    # drive_forwards_to_distance(40)
 
    # # waypoint 6
    # drive_forwards_to_distance(8)
    # turn_left_90_deg_right_laser()

    # drive_forwards_to_distance(8)
    # turn_left_90_deg_right_laser()


    # drive_forwards_to_distance(10)

    #FINISH







    # STUFF
    # turn_right_90_deg()
    # turn_right_90_deg()
    # turn_right_90_deg()
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
