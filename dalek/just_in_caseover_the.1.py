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

# when these are used in challenges they are used relative to the start position.
compass_positions = {'forward': -1, 'right': -1, 'left': -1, 'backwards': -1}


# start the sensor service.
DalekSensors = spi.SensorData()
DalekSensors.start()


def turn_right_90_deg_with_sonic():
    turnspeed = 50

    while True:
        distance = DalekSensors.left_distance
        print("{}".format(distance))
        drive.spinRight(turnspeed)
        if distance > 30:
            break


def v2_calculate_degrees_still_to_turn(start_degrees, end_degrees, direction_clockwise=True):
    current_compass =DalekSensors.compass
    result = 0
    # time.sleep(.4)
    # normalize data if not with in 360 get a new reading
    while (current_compass > 360) or (current_compass == 201):
        current_compass= DalekSensors.compass
        
       

    if direction_clockwise:
        # we go past 360/0
        if  end_degrees < start_degrees:
            
            if  end_degrees <= current_compass <=  (end_degrees +20) :
                # overshot
                result = end_degrees - current_compass
                print("cl  0     start {}  compass {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
           
            elif  end_degrees <=  current_compass :
                result = 360 - current_compass + end_degrees
                # have not passed 360 yet
                print("cl  1      start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            
            elif  current_compass <= end_degrees:
                # we have now passed 360/0 
                # but not the end point
                result = end_degrees - current_compass
                print("cl  2      start {}  compass {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            elif 0 <= current_compass <= 20:
                # we should only be here if we overshot
                result = -current_compass - (360 - end_degrees)
                print("cl  3      start {}  compass {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            else:
                print(">>>>cl  4      start {}  compass {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            

        else:
        # You should not go past 360
            if start_degrees <= current_compass <= end_degrees:
            # current_compas between  start and end
                result = end_degrees - current_compass
                print("cl+ 1      start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            elif (end_degrees + 1) <= current_compass <= (end_degrees + 20):
                #we should only ge here if we have overshot
                result = end_degrees - current_compass
                print("cl+ 2      start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            elif 0 <= current_compass <= 20:
                # we only get her if the previous condition was not met
                # and have overshot 360/0 so return negative number
                # we need to go anticlockwise a bit.
                result = -(360 - end_degrees + current_compass)
                print("cl+ 3      start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            elif (start_degrees > 20) and (current_compass < start_degrees):
                # we should only get here if the compass reading are a bit out and 
                # have a reading before we have started
                result = end_degrees - current_compass
                print("cl+ 4 err      start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            else:
                #we only should be here if the start is less than 20
                # and our compass reading was out.
                result = end_degrees - current_compass
                print("cl+ 5 err      start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
    else:
        if end_degrees > start_degrees:
            # print(" \n")
            if current_compass in range(0,start_degrees+1):
                ## not past 0 yet
                result = (360 - end_degrees) + current_compass
                print("acl- 1 start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            elif current_compass in range(end_degrees ,360):
                # past 0 but not quite there yet
                result = 360 - current_compass
                print("acl- 2 start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            elif  current_compass in range(end_degrees - 40,end_degrees-1):
                # overshot
                result = - (end_degrees - current_compass)
                print("acl- 3 start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            elif current_compass in range(start_degrees+2,start_degrees +40):
                ## compass before start
                result = (360 - end_degrees) + current_compass
                print("acl- 4 start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            else:
                print("TODO ERR")
                # start turning anyway
                result=5
                print("acl- 5 start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            
            





        
        elif end_degrees < start_degrees:
            # we need to go past 360/0
            print("not past 0")
            if current_compass in range(end_degrees,start_degrees): 
                result = current_compass - end_degrees 
                print("acl 1 start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))

            elif current_compass in range(end_degrees,(start_degrees+20)):
                #sensor  reading a bit out
                result =current_compass - end_degrees  
                print("acl 2 start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))

            elif current_compass < end_degrees:
                # we have overshot
                result = current_compass - end_degrees 
                print("acl 3 start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            elif current_compass < (start_degrees - 50):
                # overshot past 360/0
                # start_deg should be around 170ish
                result = -((360 - end_degrees) + current_compass)
                print("acl 4 start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))
            else:
                print("acl 5 error start {}  current {} end {}   output {}" .format(start_degrees,current_compass,end_degrees,result))

        else:
            # start == end // just in case
            result = 0

    return result


def get_missing_compass_positions():



    head_controller.head_move_to_center(0)
    time.sleep(.4)
    if compass_positions['forward'] == -1:
        compass_positions['forward'] = DalekSensors.compass

    if compass_positions['right'] == -1:

        head_controller.head_move_right_90deg(0)
        time.sleep(.8)
        compass_positions['right'] = DalekSensors.compass

    if compass_positions['left'] == -1:

        head_controller.head_move_left_90deg(0)
        time.sleep(.8)
        compass_positions['left'] = DalekSensors.compass

    time.sleep(.2)
    head_controller.head_move_to_center(0)



# current_relative is relative to start position

# def find_nearest_direction():
#     # when we orientate the bot at start we set postions
#     # if we use the radar of laser sensors we loose it's position
#     # so we look for the nearest one
#     result = -1
#     compass = DalekSensors.compass 
#     # if  compass_positions['left'] == compass:
#     #     result = 0
#     # elif compass_positions['center'] == compass:
#     #     result = 1
#     # elif compass_positions['right'] == compass:
#     #     result = 2
#     # else:
#     #     result = 3
    
#     # if 
    


#     return result
    


    




def turn_right_90_deg():
    turnspeed = 50

    
    # this will be hit if you have not set the backwards before
    # the start method should have set the left right and center values
    # but once set it will jump over it.
    if compass_positions['right'] == -1:
        get_missing_compass_positions()
    
    c_f = compass_positions['forward']
    c_r = compass_positions['right']

    print("left mag:{} center mag:{} right mag:{} backwards:{}" .format(
    compass_positions['left'],
    compass_positions['forward'],
    compass_positions['right'],
    compass_positions['backwards']))

    head_controller.head_move_to_center(0)
    
    print("{} {}" .format(c_f, c_r))
  
    # get your data 
    deg_to_turn = v2_calculate_degrees_still_to_turn(c_f, c_r, True)
    print("deg_to_turn:{}".format(deg_to_turn))
    
    # use the between syntax
    while -1 < deg_to_turn > 1:
        deg_to_turn = v2_calculate_degrees_still_to_turn(c_f, c_r, True)
        if deg_to_turn in range(121,300):
            print("x1")
            drive.spinRight(turnspeed+10)
        elif deg_to_turn in range(40,120):
            print("x2")
            drive.spinRight(turnspeed )
        elif deg_to_turn in range(0,39):
            print("x2")
            drive.spinRight(turnspeed -10)
        elif deg_to_turn in range(-39,-1):
            print("x3")
            drive.spinLeft(turnspeed -10)
        elif deg_to_turn in range(-40,-100):
            print("x4")
            drive.spinLeft(turnspeed )
        else:
            drive.stop()
    print("'''''''''''''''''''''''''x1'''''''''''''''''''''''''")
    turnspeed = 40
    drive.stop()
    time.sleep(.5)
    deg_to_turn = v2_calculate_degrees_still_to_turn(c_f, c_r, True)       
    while -100 < deg_to_turn > 1:
        deg_to_turn = v2_calculate_degrees_still_to_turn(c_f, c_r, True)
        if deg_to_turn in range(40,300):
            print("x11")
            drive.spinRight(turnspeed)
        elif deg_to_turn in range(0,39):
            print("x12")
            drive.spinRight(turnspeed -10)
        elif deg_to_turn in range(-39,-1):
            print("x13")
            drive.spinLeft(turnspeed -10)
        elif deg_to_turn in range(-40,-100):
            print("x14")
            drive.spinLeft(turnspeed )
        else:
            drive.stop()
    print("'''''''''''''''''''''''''x2'''''''''''''''''''''''''")
    turnspeed = 40
    drive.stop()
    time.sleep(.5)
    deg_to_turn = v2_calculate_degrees_still_to_turn(c_f, c_r, True)       
    while -100 < deg_to_turn > 1:
        deg_to_turn = v2_calculate_degrees_still_to_turn(c_f, c_r, True)
        if deg_to_turn in range(40,300):
            print("x11")
            drive.spinRight(turnspeed)
        elif deg_to_turn in range(0,39):
            print("x12")
            drive.spinRight(turnspeed -10)
        elif deg_to_turn in range(-39,-1):
            print("x13")
            drive.spinLeft(turnspeed -10)
        elif deg_to_turn in range(-40,-100):
            print("x14")
            drive.spinLeft(turnspeed )
        else:
            drive.stop()

    drive.stop()


    # swap  compass positions
    new_position =[compass_positions['left'],compass_positions['forward'],compass_positions['right'],compass_positions['backwards']]
    compass_positions['left'] = new_position[1]
    compass_positions['forward'] = new_position[2]
    compass_positions['right'] = new_position[3]
    compass_positions['backwards'] = new_position[0]

    print("END {} {} {}" .format(c_f, c_r, DalekSensors.compass))
    print("left mag:{} center mag:{} right mag:{} backwards:{}" .format(
        compass_positions['forward'],
        compass_positions['left'],
        compass_positions['right'],
        compass_positions['backwards']))
    time.sleep(1)
    final_val = DalekSensors.compass
    print("final {} {}" .format( final_val, compass_positions['right'] -final_val ))



def turn_left_90_deg():
    

    if compass_positions['left'] ==-1:
        get_missing_compass_positions()
    c_f =  compass_positions['forward']
    c_l = compass_positions['left']

    head_controller.head_move_to_center(0)

    print("{} {}" .format(c_f, c_l))

    # deg_to_turn = v2_calculate_degrees_still_to_turn(c_f, c_l, False)

    # print("deg_to_turn:{}".format(deg_to_turn))
    def move(_turnspeed):
        turnspeed = _turnspeed
        deg_to_turn = v2_calculate_degrees_still_to_turn(c_f, c_l, False)
        while -1 < deg_to_turn > 1:
            if deg_to_turn in range(121,300):
                print("L_1")
                time.sleep(.4)
                drive.spinLeft(turnspeed+10)

            elif deg_to_turn in range(40,120):
                print("L_2")
                drive.spinLeft(turnspeed )

            elif deg_to_turn in range(0,39):
                print("L_3")
                drive.spinLeft(turnspeed -10)
            elif deg_to_turn in range(-39,-1):
                print("L_4")
                drive.spinRight(turnspeed -10)
            elif deg_to_turn in range(-40,-100):
                print("L_5")
                drive.spinRight(turnspeed )
            else:
                drive.stop()
            deg_to_turn = v2_calculate_degrees_still_to_turn(c_f, c_l, False)
        drive.stop()
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    move(50)
    time.sleep(.4)
    move(40)
    time.sleep(.4)
    move(40)


    new_position =[compass_positions['left'],compass_positions['forward'],compass_positions['right'],compass_positions['backwards']]
    compass_positions['left'] = new_position[3]
    compass_positions['forward'] = new_position[0]
    compass_positions['right'] = new_position[1]
    compass_positions['backwards'] = new_position[2]
         
    # ALL done
    # just debug

    time.sleep(1)
    _compass =DalekSensors.compass
    print("left mag:{} center mag:{} right mag:{} backwards:{} ---- final {} diff:{}" .format(
        compass_positions['left'],
        compass_positions['forward'],
        compass_positions['right'],
        compass_positions['backwards'],
        _compass,   _compass - compass_positions['left']  
        ))
    

   




def calibrate_compass():
    head_controller.leds_change_color(head_controller.leds_color['yellow'])
    # print("point your bot in the forward position.")
    head_controller.head_move_to_center(0)
    time.sleep(.4)
    compass_positions['forward'] = DalekSensors.compass

    if compass_positions['left'] == -1:
        head_controller.head_move_left_90deg(0)
        time.sleep(1)
        compass_positions['left'] = DalekSensors.compass

    if compass_positions['right'] == -1:
        head_controller.head_move_right_90deg(0)
        time.sleep(1)
        compass_positions['right'] = DalekSensors.compass

    # forward, left and right done
    head_controller.head_move_to_center(0)
    time.sleep(.3)
    head_controller.leds_change_color(head_controller.leds_color['green'])
    print("left mag:{} center mag:{} right mag:{} backwards:{}" .format(
        compass_positions['left'],
        compass_positions['forward'],
        compass_positions['right'],
        compass_positions['backwards']))

    # TODO: turn dalek and get backwards...if needed


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
        # get the speed to drive at
        speed = CalculateSpeedToDrive(DalekSensors.front_distance, distance)
        if DalekSensors.front_distance <= distance:
            drive.backward(speed)
            print("drive_backwards()")
        else:
            drive.paddleForward(speed, speed)
    drive.stop()

    # counter+=1
    # print("counter:{}".format(counter))


def straighten_up():
    print("{} {} {}".format(DalekSensors.laser_front_left,
                            DalekSensors.front_distance, DalekSensors.laser_front_right))

    lz_left = DalekSensors.laser_front_left
    lz_right = DalekSensors.laser_front_right
    while lz_left != lz_right:
        if lz_left > lz_right:
            drive.spinRight(30)
        elif lz_left < lz_right:
            drive.spinLeft(30)
        time.sleep(.1)
        print("{} {} ".format(lz_left, lz_right))

        lz_left = DalekSensors.laser_front_left
        lz_right = DalekSensors.laser_front_right

    print("{} {} ".format(lz_left, lz_right))
    drive.stop()
# this uses the Rear ultrasonic sensor.


def drive_backwards_to_distance(distance=distance_to_wall):

    print("driveBackwards()")

    while DalekSensors.rear_distance != distance:
        dalekSpeed = CalculateSpeedToDrive(
            DalekSensors.rear_distance, distance)

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


def driveParallelToRightWall(distanceToWall):
    pass


def driveParallelToWallsInCenterToFrontPingDistance(distanceToWall=None):
    pass


def dispose():
    drive.cleanup()


def turn_right_90_deg_left_laser():
    lz_left = DalekSensors.laser_front_left
    lz_center = DalekSensors.front_distance
    lz_right = DalekSensors.laser_front_right

    print("{} {} {}" .format(lz_left, lz_center, lz_right))

    while DalekSensors.front_distance < 80:
        drive.spinRight(40)

    while (lz_left < 40):
        lz_left = DalekSensors.laser_front_left
        lz_center = DalekSensors.front_distance
        lz_right = DalekSensors.laser_front_right
        print("{} {} {}" .format(lz_left, lz_center, lz_right))
        drive.spinRight(40)
    drive.stop()
    
    # swap  compass positions
    new_position =[compass_positions['left'],compass_positions['forward'],compass_positions['right'],compass_positions['backwards']]
    compass_positions['left'] = new_position[1]
    compass_positions['forward'] = new_position[2]
    compass_positions['right'] = new_position[3]
    compass_positions['backwards'] = new_position[0]


def turn_left_90_deg_right_laser():
    lz_left = DalekSensors.laser_front_left
    lz_center = DalekSensors.front_distance
    lz_right = DalekSensors.laser_front_right

    print("{} {} {}" .format(lz_left, lz_center, lz_right))

    while DalekSensors.front_distance < 80:
        drive.spinLeft(40)

    while (lz_right < 50):
        lz_left = DalekSensors.laser_front_left
        lz_center = DalekSensors.front_distance
        lz_right = DalekSensors.laser_front_right
        print("{} {} {}" .format(lz_left, lz_center, lz_right))
        drive.spinLeft(40)

    drive.stop()
    new_position =[compass_positions['left'],compass_positions['forward'],compass_positions['right'],compass_positions['backwards']]
    compass_positions['left'] = new_position[3]
    compass_positions['forward'] = new_position[0]
    compass_positions['right'] = new_position[1]
    compass_positions['backwards'] = new_position[2]


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


# waypoint starts when you arrive at the point, not to get there

def start():
    calibrate_compass()
    drive_forwards_to_distance(9)
    turn_right_90_deg()
    drive_forwards_to_distance(9)
    time.sleep(1)

    # turn_right_90_deg_left_laser()
    turn_right_90_deg()
    drive_forwards_to_distance(9)
    time.sleep(1)

    turn_right_90_deg()
    # turn_right_90_deg_left_laser()
    drive_forwards_to_distance(9)
    time.sleep(1)

    # turn_right_90_deg_left_laser()
    drive_forwards_to_distance(9)
    time.sleep(1)
    
    # turn_right_90_deg_left_laser()
    turn_right_90_deg()
    drive_forwards_to_distance(9)
    time.sleep(1)
    




# def waypoint_1():
#     drive_forwards_to_distance(45)


# def waypoint_2():
#     drive_forwards_to_distance(8)


# def waypoint_3():
#     straighten_up()
#     turn_right_90_deg()
#     drive_forwards_to_distance(40)


# def waypoint_4():
#     turn_left_90_deg()
#     drive_forwards_to_distance(10)


# def waypoint_5():
#     turn_left_90_deg()
#     drive_forwards_to_distance(10)


# def waypoint_6():
#     turn_right_90_deg_left_laser()
#     drive_forwards_to_distance(8)


def main():
    start()
    # print_compass()
    
    # drive_forwards_to_distance(10)
    # drive_backwards_to_distance(10)
    # turn_right_90_deg()
    # turn_right_90_deg()
    # drive_forwards_to_distance(10)
    # straighten_up()
    # # get_missing_compass_positions()
    # turn_left_90_deg()
    # turn_left_90_deg()
    # drive_forwards_to_distance(10)
    # turn_right_90_deg('backwards','left'  )
    # turn_right_90_deg('left','forward'  )



    # turn_right_90_deg(compass_positions['right'],compass_positions['backwards']  )
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
    # get_compass_turn_right_90_deg()
    # get_compass_turn_right_90_deg()
    # get_compass_turn_right_90_deg()
    # get_compass_turn_right_90_deg()
    # turn_right_90_deg_with_sonic()
    # drive_backwards_to_distance() 
    # drive_forwards_to_distance(15)
    # straighten_up()
    # calibrate_compass()

    # start()
    # waypoint_1()
    # waypoint_2()
    # waypoint_3()
    # waypoint_4()
    # waypoint_5()
    # waypoint_6()


def print_compass():
    print("L F R Rear {} {} {} {}".format(
        compass_positions['left'],
        compass_positions['forward'],
        compass_positions['right'],
        compass_positions['backwards']))


# def turn_left():
#     turnspeed = 50
#     while DalekSensors.compass > (145+5):
#         drive.spinLeft(turnspeed)
#         time.sleep(.2)

#     print(DalekSensors.compass)
#     drive.stop()
#     print("Stop")
#     time.sleep(1)
#     print(DalekSensors.compass)
#     DalekSensors.stop_running()


if __name__ == "__main__":

    main()
    drive.stop()
    head_controller.leds_change_color(head_controller.leds_color['off'])
    drive.cleanup()
    DalekSensors.stop_running()
