#!/usr/bin/python3
if __name__ == "__main__":
    '''
    This if statement is needed for testing, to locate the modules needed
    if we are running the file directly.
    '''
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import spidev
import time
from dalek import debug
import threading
from statistics import mode


'''
If you get an error like the following you forgot to call the init() function.

Traceback (most recent call last):
  File "dalek/spi.py", line 134, in <module>
    main()
  File "dalek/spi.py", line 127, in main
    print(read_device_1_data())
  File "dalek/spi.py", line 80, in read_device_1_data
    piSensors['frontPing'] = get_sensor_data(0)
  File "dalek/spi.py", line 67, in get_sensor_data
    except expression as identifier:
NameError: name 'expression' is not defined
'''


# make sure you install spidev
# http://www.takaitra.com/posts/492

# SPEED	SPI.MAX_SPEED_HZ VALUE
# 25.0 MHz  	125000000
# 62.5 MHz	  62500000
# 31.2 MHz   	31200000
# 15.6 MHz   	15600000
# 7.8 MHz    	7800000 the arduino clock rate is 8MHz
# 3.9 MHz    	3900000
# 1953 kHz  	1953000
# 976 kHz	    976000
# 488 kHz    	488000
# 244 kHz   	244000
# 122 kHz	    122000
# 61 kHz	    61000
# 30.5 kHz   	30500
# 15.2 kHz  	15200
# 7629 Hz   	7629
# SpiSetup = False
spi = spidev.SpiDev()

# Obsolete


def init(device=0):
    # left here from previous versions
    pass


def open_spi_device(device=0):
    global spi
    spi.open(0, device)  # using bus 1
    spi.max_speed_hz = 61000
    spi.mode = 0b00


def close_spi_device():
    global spi
    spi.close()


def get_sensor_data(_sensorNumber):

    dataToSend = [_sensorNumber, 200, 201, 255]
    try:

        receivedBytes = spi.xfer(dataToSend)
        sensorValue = (receivedBytes[2] << 8) + receivedBytes[3]
        return sensorValue
    except:
        debug.print_to_all_devices(
            "error geting data from Arduino via spi bus")

def change_mode_on_device_(mode):
    # mode 10: all data is read
    # mode 11: left ping only
    # mode 12: right ping only
    # mode 13: center ping only
    # mode 14: compass only
    # mode 15: all data is read and debug output
    dataToSend = [10, mode , 0, 0]
    try:

        receivedBytes = spi.xfer(dataToSend)
        # sensorValue = (receivedBytes[2] << 8) + receivedBytes[3]
        # return sensorValue
    except:
        debug.print_to_all_devices(
            "error geting data from Arduino via spi bus")
    


def get_mag():
    open_spi_device()
    data = get_sensor_data(4)
    close_spi_device()
    return data


def read_device_1_data():

    # create the return data variable
    open_spi_device()
    # piSensors = {'frontPing': 0, 'rearPing': 0,
    #              'left_distance': 0, 'right': 0, 'compass': 0}
    piSensors = {'rear_distance': 0,'left_distance': 0, 'right_distance': 0, 'compass': 0}
    # piSensors['frontPing'] = get_sensor_data(0)
    # time.sleep(.00001)
    piSensors['rear_distance'] = get_sensor_data(3)
    # time.sleep(.00001)
    piSensors['left_distance'] = get_sensor_data(1)
    time.sleep(.00001)
    piSensors['right_distance'] = get_sensor_data(2)
    time.sleep(.00001)
    piSensors['compass'] = get_sensor_data(4)

    close_spi_device()
    return piSensors


def read_device_2_data():
    open_spi_device(1)
    laser_sensors = {
        'left_laser': 0,
        'center_laser': 0,
        'right_laser': 0
    }
    for x in range(0, 3):
        data = get_sensor_data(x)
        while data > 819 or data == 201:
            data = get_sensor_data(x)
        laser_sensors[x] = int(data)

    close_spi_device()
    return laser_sensors


class CompassData(threading.Thread):
    running = True

    def __init__(self):
        super().__init__()
        self.data = 0
        open_spi_device()

    def stop_running(self):
        '''
        when this is called it ends this thread
        '''
        close_spi_device()
        self.running = False

    def run(self):

        while self.running:

            self.data = get_sensor_data(4)
            # print(self.data)
            time.sleep(.2)


# class GetLeftSensor(threading.Thread):
#     running = True

#     def __init__(self):
#         super().__init__()
#         self.left_distance = 0

#     def stop_running(self):
#         '''
#         when this is called it ends this thread
#         '''
#         self.running = False
        
#     def run(self):
#         while self.running:
#             try:
#                 pass
#             except:
#                 pass


class SensorData(threading.Thread):
    running = True

    def __init__(self):
        super().__init__()
        # self.frontPing = 0
        self.rear_distance = 0
        self.left_distance = 0
        self.right_distance = 0
        self.laser_front_left = 0
        self.front_distance = 0
        self.laser_front_right = 0
        self.compass = 0

    def stop_running(self):
        '''
        when this is called it ends this thread
        '''
        self.running = False

    def run(self):

        # get seven readings and average them out using mode
        # to get a more accurate reading
        while self.running:
            # start_time = time.time()
            # s1 = read_device_1_data()
            # # time.sleep(.02)
            # s2 = read_device_1_data()
            # # time.sleep(.02)
            # s3 = read_device_1_data()
            # # time.sleep(.02)
            # s4 = read_device_1_data()
            # # time.sleep(.02)
            # s5 = read_device_1_data()
            # s6 = read_device_1_data()
            # s7 = read_device_1_data()

            try:
                # front = mode([s1['frontPing'],
                #               s2['frontPing'],
                #               s3['frontPing'],
                #               s4['frontPing'],
                #               s5['frontPing'],
                #               s6['frontPing'],
                #               s7['frontPing']
                #               ])

                # right = mode([s1['right'],
                #               s2['right'],
                #               s3['right'],
                #               s4['right'],
                #               s5['right'],
                #               s6['right'],
                #               s7['right']])

                # left = mode([s1['left_distance'],
                #              s2['left_distance'],
                #              s3['left_distance'],
                #              s4['left_distance'],
                #              s5['left_distance'],
                #              s6['left_distance'],
                #              s7['left_distance']])

                # rear = mode([s1['rearPing'],
                #              s2['rearPing'],
                #              s3['rearPing'],
                #              s4['rearPing'],
                #              s5['rearPing'],
                #              s6['rearPing'],
                #              s7['rearPing']])

                # compass = mode([s1['compass'],
                #                 s2['compass'],
                #                 s3['compass'],
                #                 s4['compass'],
                #                 s5['compass'],
                #                 s6['compass'],
                #                 s7['compass']])
                data_dev1 = read_device_1_data()
                laser_sensors = read_device_2_data()

            except:
                print("unknown error.")

            # now read from the laser sensors

            # print("left_laser {} center_laser {} right_laser {} left:{} right:{} compass:{} rear:{}".format(
            #     laser_sensors[0],
            #     laser_sensors[1],
            #     laser_sensors[2],
            #     data_dev1['left_distance'],
            #     data_dev1['right_distance'],
            #     data_dev1['compass'],
            #     data_dev1['rear_distance']))

        
            # self.frontPing = front
            self.left_distance = data_dev1['left_distance']
            self.right_distance = data_dev1['right_distance']
            self.rear_distance= data_dev1['rear_distance']
            self.compass = data_dev1['compass']
            self.laser_front_left= laser_sensors[0]
            self.front_distance = laser_sensors[1]
            self.laser_front_right = laser_sensors[2]

            # time.sleep(1)


def test():
    T = time.time()
    data = read_device_1_data()
    T2 = time.time()

    debug.print_to_all_devices(data)
    debug.print_to_all_devices("time taken {}" .format(T2 - T))


def main():
    '''
    This test that things are working, it just prints the Arduino's readings to stout.
    '''

    # init()
    try:
        sensordata = SensorData()
        sensordata.start()
    except:
        pass

#######################################################################################


if __name__ == "__main__":
    main()
else:
    debug.print_to_all_devices("Importing DalekSpi.py")
