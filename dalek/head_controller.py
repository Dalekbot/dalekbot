#!/usr/bin/python3
if __name__ == "__main__":
    '''
    This if statement is needed for testing, to locate the modules needed
    if we are running the file directly.
    '''
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import smbus
import time
bus = smbus.SMBus(1)


address = 0x08

# send two bytes of data to reset the arduino and
# signal that a new dataset is about to come
# these can be anything but need to be the same on both ends.

# byte 1 = 129 -> start of transmission
# byte 2 = 254 -> start of transmission

# now arduino is waiting for data.

# byte 3 : device number for new data.
# byte 4 = new value 1
# byte 5 = new value 2
# byte 6 :new value 3  / not used
# byte 7: new value 4  / not used
# byte 8 :new value 5  / not used

# time between 8 bytes if data
# to allow device to execute the required function.
# If you get an error, the data is being sent too quickly
# to execute on the Arduino so use this variable
i2c_timeing_delay = .1

# these can be changed to match your servo initial offset position.
head_device_id = 2  # this is the id on the Arduino
head_right_90deg_position = 16
head_left_90deg_position = 170
head_center_position = 93
head_movement_speed = 10

eye_device_id = 1  # this is the id on the Arduino
eye_top_max_position = 95    # up
eye_bottom_min_position = 45  # down
eye_mid_position = 70
eye_movement_speed = 10

leds_device_id = 3
leds_color = { 'off':0, 'green':1, 'red':2, 'yellow':3, 'blue':4,'white':5}
leds_current_color = 1
leds_are_flashing = False

def send_data_to_head(int_1=0,int_2=0,int_3=0,int_4=0,int_5=0):
    #TODO this should be a queue
    success = False

    try:
        bus.write_byte(address, int_1) 
    except:
        print("i2c sending error 1")
    try:
        bus.write_byte(address, int_2) 
    except:
        print("i2c sending error 2")
    try:
        bus.write_byte(address, int_3) 
    except:
        print("i2c sending error 3")
    try:
        bus.write_byte(address, int_4) 
    except:
        print("i2c sending error 4")
    try:
        bus.write_byte(address, int_5) 
    except:
        print("i2c sending error 5")
    

        # not used but sent to complete the 8 bits required.
    time.sleep(i2c_timeing_delay)
    try:
        bus.write_byte(address, 0) 
    except:
        print("i2c sending error 6")
    time.sleep(i2c_timeing_delay)
    try:
        bus.write_byte(address, 0) 
    except:
        print("i2c sending error 7")
    time.sleep(i2c_timeing_delay)
    try:
        bus.write_byte(address, 0) 
        # if we get here then it succeeded
        success = True
    except:
        print("i2c sending error 8")


        
    
    time.sleep(i2c_timeing_delay)
    return success

########
# LED's


def leds_flash(on=True):
    flash = 1      # start flashing the leds
    if on == False:
        flash =0   # stop flashing the leds
    
    send_data_to_head(129,254,4,flash,0)

def leds_change_color(color):
    time.sleep(i2c_timeing_delay)
    send_data_to_head(129,254,leds_device_id,color)

def leds_cycle_colors():
    # increment colors, when you reach the end, set to start.
    global leds_current_color
    leds_current_color +=1
    if leds_current_color == 6:
        leds_current_color = 1
    send_data_to_head(129,254,leds_device_id,leds_current_color)

def leds_toggle_flash():
    global leds_are_flashing
    if leds_are_flashing:
        leds_are_flashing =False
        send_data_to_head(129,254,4,0,0)
    else:
        leds_are_flashing = True
        send_data_to_head(129,254,4,1,0)

#### HEAD 

def head_rotate(new_position,speed=head_movement_speed):
    send_data_to_head(129,254,head_device_id,new_position,speed)
  

def head_stop(): 
    send_data_to_head(129,254,5)

def head_move_to_center(speed = head_movement_speed):
    head_rotate(head_center_position,speed)


def head_move_right_90deg(speed = head_movement_speed):
    head_rotate(head_right_90deg_position,speed)


def head_move_left_90deg(speed = head_movement_speed):
    head_rotate(head_left_90deg_position,speed)

def head_no():
    timing = .6
    head_rotate(head_center_position+25)
    time.sleep(timing)
    head_rotate(head_center_position-25) 
    time.sleep(timing)
    head_rotate(head_center_position+25)
    time.sleep(timing)
    head_rotate(head_center_position-25)
    time.sleep(timing)
    head_rotate(head_center_position) 

#### EYE
def eye_move(new_position,speed=0):

    if (speed == 0):
        speed = eye_movement_speed
    if new_position > eye_top_max_position:
        new_position = eye_top_max_position
    if new_position < eye_bottom_min_position:
        new_position = eye_bottom_min_position

    send_data_to_head(129,254,eye_device_id,new_position,speed)

def eye_stop():
    send_data_to_head(129,254,6)

def eye_move_to_top():
    eye_move(eye_top_max_position)

def eye_move_to_bottom():
    eye_move(eye_bottom_min_position)

def eye_move_to_center():
    eye_move(eye_mid_position+15)
    time.sleep(.3)
    eye_move(eye_mid_position)

def eye_waggle():
    eye_move(eye_mid_position+25)
    time.sleep(.3)
    eye_move(eye_mid_position-10)
    time.sleep(1)
    eye_move(eye_mid_position+25)
    time.sleep(1.2)
    eye_move(eye_mid_position)



def main():

    leds_flash(True)
    leds_change_color(leds_color['green'])

    # eye_move_to_center()
    head_move_to_center()
    time.sleep(1)
    # time.sleep(1)
    # eye_move_to_top()
    # leds_flash(False)
    # leds_change_color(leds_color['red'])
    head_move_left_90deg()
    time.sleep(1)


    head_move_right_90deg()

    # head_left_90deg_position()
    time.sleep(.5)
    head_stop()
    print("stop")
    time.sleep(.5)
    # eye_move_to_center()
    # eye_move_to_bottom() 
    head_move_right_90deg()

    time.sleep(1)
    # head_no()
    head_move_to_center()
    # eye_waggle()
    # leds_change_color(leds_color['blue'])
    # time.sleep(1)
    # time.sleep(i2c_timeing_delay)
    # leds_change_color(leds_color['yellow'])

    # # for x in range (1,20):
    # leds_change_color(leds_color['green'])
    time.sleep(1)
    leds_change_color(leds_color['red'])
    time.sleep(i2c_timeing_delay)
    leds_flash(False)
    # time.sleep(4) 
    #     leds_change_color(leds_color['off'])



if __name__ == "__main__": 
    main()
