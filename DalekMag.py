#Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# LSM303DLHC
# This code is designed to work with the LSM303DLHC_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time
import math
# Get I2C bus
bus = smbus.SMBus(1)


# use this to read from the mag directly.
   

# time.sleep(0.5)
def getMag():


    # LSM303DLHC Mag address, 0x1E(30)
    # Select MR register, 0x02(02)
    #		0x00(00)	Continous conversion mode
    bus.write_byte_data(0x1E, 0x02, 0x00)
    # LSM303DLHC Mag address, 0x1E(30)
    # Select CRA register, 0x00(00)
    #		0x10(16)	Temperatuer disabled, Data output rate = 15Hz
    bus.write_byte_data(0x1E, 0x00, 0x10)
    # LSM303DLHC Mag address, 0x1E(30)
    # Select CRB register, 0x01(01)
    #		0x20(32)	Gain setting = +/- 1.3g
    bus.write_byte_data(0x1E, 0x01, 0x20)


    # LSM303DLHC Mag address, 0x1E(30)
    # Read data back from 0x03(03), 2 bytes
    # X-Axis Mag MSB, X-Axis Mag LSB
    data0 = bus.read_byte_data(0x1E, 0x03)
    data1 = bus.read_byte_data(0x1E, 0x04)
    
    # Convert the data
    xMag = data0 * 256 + data1
    if xMag > 32767 :
    	xMag -= 65536
    
    # LSM303DLHC Mag address, 0x1E(30)
    # Read data back from 0x05(05), 2 bytes
    # Y-Axis Mag MSB, Y-Axis Mag LSB
    data0 = bus.read_byte_data(0x1E, 0x07)
    data1 = bus.read_byte_data(0x1E, 0x08)
    
    # Convert the data
    yMag = data0 * 256 + data1
    if yMag > 32767 :
    	yMag -= 65536
    
    # Output data to screen
    # print "Magnetic field in X-Axis : %d" %xMag
    # print "Magnetic field in Y-Axis : %d" %yMag
    Pi = 3.14159
    
    heading =int( (math.atan2(yMag,xMag) * 180) / Pi)
    if heading < 0:
          heading = 360 + heading
    print('heading:{}'.format(heading))
    # print "Magnetic field in Z-Axis : %d" %zMag
    return heading

while True:
    getMag()  
    time.sleep(1)   


    # __main__ Code
# #======================================================================	   
    
# if __name__ == "__main__":
#     print("\n\nThis file cannot be run directly. It is intended to be imported\n\n")
# else:
#     print("\n\nImporting DalekMag.py")
    
# # End of __main__ Code
# #======================================================================