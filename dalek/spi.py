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
    except expression as identifier:
        debug.print_to_all_devices(
            "error geting data from Arduino via spi bus")


def get_mag():
    open_spi_device()
    return get_sensor_data(4)
    close_spi_device()


def read_device_1_data():

    # create the return data variable
    open_spi_device()
    piSensors = {'frontPing': 0, 'rearPing': 0,
                 'leftPing': 0, 'rightPing': 0, 'compass': 0}
    piSensors['frontPing'] = get_sensor_data(0)
    time.sleep(.00001)
    piSensors['rearPing'] = get_sensor_data(3)
    time.sleep(.00001)
    piSensors['leftPing'] = get_sensor_data(2)
    time.sleep(.00001)
    piSensors['rightPing'] = get_sensor_data(1)
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


class SensorData(threading.Thread):
    running = True

    def __init__(self):
        super().__init__()
        self.frontPing = 0
        self.rearPing = 0
        self.leftPing = 0
        self.rightPing = 0
        self.laser_left = 0
        self.laser_center = 0
        self.laser_right = 0

    def stop_running(self):
        '''
        when this is called it ends this thread
        '''
        self.running = False

    def run(self):

        # get seven readings and average them out using mode
        # to get a more accurate reading
        while self.running:
            start_time = time.time()
            s1 = read_device_1_data()
            # time.sleep(.02)
            s2 = read_device_1_data()
            # time.sleep(.02)
            s3 = read_device_1_data()
            # time.sleep(.02)
            s4 = read_device_1_data()
            # time.sleep(.02)
            s5 = read_device_1_data()
            s6 = read_device_1_data()
            s7 = read_device_1_data()

            try:
                front = mode([s1['frontPing'],
                              s2['frontPing'],
                              s3['frontPing'],
                              s4['frontPing'],
                              s5['frontPing'],
                              s6['frontPing'],
                              s7['frontPing']
                              ])

                right = mode([s1['rightPing'],
                              s2['rightPing'],
                              s3['rightPing'],
                              s4['rightPing'],
                              s5['rightPing'],
                              s6['rightPing'],
                              s7['rightPing']])

                left = mode([s1['leftPing'],
                             s2['leftPing'],
                             s3['leftPing'],
                             s4['leftPing'],
                             s5['leftPing'],
                             s6['leftPing'],
                             s7['leftPing']])

                rear = mode([s1['rearPing'],
                             s2['rearPing'],
                             s3['rearPing'],
                             s4['rearPing'],
                             s5['rearPing'],
                             s6['rearPing'],
                             s7['rearPing']])

                compass = mode([s1['compass'],
                                s2['compass'],
                                s3['compass'],
                                s4['compass'],
                                s5['compass'],
                                s6['compass'],
                                s7['compass']])

            except:
                print("unknown error.")

            # now read from the laser sensors
            laser_sensors = read_device_2_data()

            # print("left_laser {} center_laser {} right_laser {} front:{} right:{} left:{} rear:{} compass:{} time:{} ".format(
            #                                                                                                             laser_sensors[0],
            #                                                                                                             laser_sensors[1],
            #                                                                                                             laser_sensors[2],
            #                                                                                                             front,
            #                                                                                                             right,
            #                                                                                                             left,
            #                                                                                                             rear,
            #                                                                                                             compass,
            #                                                                                                             time.time() - start_time))

            # if  laser_sensors[0] == laser_sensors[2]:
            #     print("=== {}" .format(laser_sensors[1]))
            #     print("left_laser center_laser right_laser: {} {}  {}  =====".format( laser_sensors[0], laser_sensors[1], laser_sensors[2]))
            # else:
            #     print("left_laser center_laser right_laser: {} {}  {} ".format( laser_sensors[0], laser_sensors[1], laser_sensors[2]))

            # if  laser_sensors[1]< 90:
            #     if  (laser_sensors[0] == laser_sensors[2]):
            #         print("forward {}" .format(laser_sensors[1]))
            #     elif laser_sensors[0] > laser_sensors[2]:

            #         print("right {} {} {} {} {} {}".format( laser_sensors[0], laser_sensors[1], laser_sensors[2],compass, left, right))
            #     else:
            #         print("left {} {} {} {} {} {}".format( laser_sensors[0], laser_sensors[1], laser_sensors[2],compass, left, right))

            self.frontPing = front
            self.leftPing = left
            self.rightPing = right
            self.rearPing = rear
            self.compass = compass
            self.laser_left = laser_sensors[0]
            self.laser_center = laser_sensors[1]
            self.laser_right = laser_sensors[2]

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
    except expression as identifier:
        pass

#######################################################################################


if __name__ == "__main__":
    main()
else:
    debug.print_to_all_devices("Importing DalekSpi.py")
