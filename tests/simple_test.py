import time
import math


# this is based on the Adafruit libray code
# it is not used anyware but left in for testing things work.
# you will need to install the adafruit lib and connect up the i2c on the device.

# Import the LSM303 module.
import Adafruit_LSM303

# Create a LSM303 instance.
lsm303 = Adafruit_LSM303.LSM303()


def getMag():
   # Read the X, Y, Z axis acceleration values and print them.
    accel, mag = lsm303.read()
    # Grab the X, Y, Z components from the reading and print them out.
   # accel_x, accel_y, accel_z = accel
    mag_x, mag_z, mag_y = mag
    # print('Accel X={0}, Accel Y={1}, Accel Z={2}, Mag X={3}, Mag Y={4}, Mag Z={5}'.format(
    #       accel_x, accel_y, accel_z, mag_x, mag_y, mag_z))
    # Wait half a second and repeat.
    Pi = 3.14159

    # foo = (math.atan2(accel_y,mag_x) * 180) / Pi
    # print(foo)

    headding = int((math.atan2(mag_y, mag_x) * 180) / Pi)
    if headding < 0:
        headding = 360 + headding
    return headding


# while True:
#     headding = getMag()
#     print('headding:{} '.format(headding))
#     # time.sleep(0.05)

    # __main__ Code
#======================================================================	   
thisfilename = "simpletest.py"   
if __name__ == "__main__":
    print("\n\nThis file ({}) cannot be run directly. It is intended to be imported\n\n" .format(thisfilename))
else:
    print("\n\nImporting {}" .format(thisfilename)) 
    
# End of __main__ Code
#======================================================================
