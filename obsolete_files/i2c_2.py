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
speed_delay = 6


def send_data_to_head_Arduino(device_number, 
    new_value_1, 
    new_value_2,
    new_value_3=0,
    new_value_4=0,
    new_value_5=0):
    try:
        bus.write_byte(address, 129)
        bus.write_byte(address, 254)
        bus.write_byte(address, device_number)
        bus.write_byte(address, new_value_1)
        bus.write_byte(address, new_value_2)

        # not used but sent to complete the 8 bits required.
        bus.write_byte(address, new_value_3)
        bus.write_byte(address, new_value_4)
        bus.write_byte(address, new_value_5)
    except:
        print("i2c sending error")


# send_data_to_head_Arduino(1,90,10)
# time.sleep(1)
# send_data_to_head_Arduino(1,68,10)
# time.sleep(.5)
send_data_to_head_Arduino(2,172,0)
time.sleep(1)
send_data_to_head_Arduino(2,0,0)
time.sleep(.5)
# send_data_to_head_Arduino(1,70,10)
time.sleep(1)
send_data_to_head_Arduino(2,85,10)
time.sleep(.2)
send_data_to_head_Arduino(2,172,0) 
time.sleep(1)
send_data_to_head_Arduino(2,0,0)
time.sleep(.5)
# send_data_to_head_Arduino(1,70,10)
time.sleep(1)
send_data_to_head_Arduino(2,0,10)