#!/usr/bin/python

import spidev
import time

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
SpiSetup = False
spi = spidev.SpiDev()


def init(speed=None):
    global SpiSetup,spi

    spi.open(0, 0)  # using bus 1

    if speed != None:
      try:
        spi.max_speed_hz = speed
        SpiSetup = True
      except expression as identifier:
          pass
    else:
      # set the default value
      spi.max_speed_hz = 61000
      SpiSetup = True

    spi.mode = 0b00  # another mode is spi.mode = 0b01
    print("spi bus speed set to:{} spi mode {}" .format( spi.max_speed_hz, spi.mode))

def getSensorData(_sensorNumber):
    global spi
    dataToSend = [_sensorNumber, 200, 201, 255]
    try:
        
        receivedBytes = spi.xfer(dataToSend)
        sensorValue = (receivedBytes[2] << 8) + receivedBytes[3]
        return sensorValue
    except expression as identifier:
        print("error geting data from Arduino via spi bus")

def getMag():
    return getSensorData(4)


def readDevice1Data():
  global SpiSetup,spi
 
  # create the return data variable
  piSensors = {'frontPing': 0, 'rearPing': 0,
               'leftPing': 0, 'rightPing': 0, 'compass': 0}
  if not SpiSetup :
    print("\nYou need to initialize the SPI bus first use the use the init() function")
    return piSensors
  # dataToSend [ first bit= device that we want to read, 200 and 201 codes 
  # lets the remote device know that it needs to process the data , 255 is the end bit ]
  dataToSend = [0, 200, 201, 255]
  for i in range(5):
    ## assign the sensor number
    dataToSend[0] = i
    # receivedBytes = [first bit is not used as it was set on previous request (always 0),
    # device number, high bit shifted value, low bit shifted value]
    receivedBytes = spi.xfer(dataToSend)
    # shift our data back and add together for our sensor value.
    # it is now a 16 bit int.
    sensorValue = (receivedBytes[2] << 8) + receivedBytes[3]
    if receivedBytes[1] == 0:  # frontPing
        piSensors['frontPing'] = sensorValue
    elif receivedBytes[1] == 1:  # rearPing
        piSensors['leftPing'] = sensorValue
    elif receivedBytes[1] == 2:  # leftPing 
        piSensors['rightPing'] = sensorValue
    elif receivedBytes[1] == 3:  # rightPing
        piSensors['rearPing'] = sensorValue
    elif receivedBytes[1] == 4:  # compass
        piSensors['compass'] = sensorValue
    else:
        print("Sensor Error. Remote Sensor:{} with value:{} not known" .format(
            receivedBytes[1], sensorValue))
    if i == 4:
        count = 0
        # print(piSensors)
    # change this if you get errors.
    time.sleep(.00001)
  return piSensors

def test():
   T = time.time()
   readDevice1Data()
   T2 = time.time()
   print("time taken {}" .format(T2 - T)) 


#======================================================================	   
    
if __name__ == "__main__":
    print("\n\nThis file 'DalekSpi.py' cannot be run directly. It is intended to be imported\n\n")
else:
    print("\n\nImporting DalekSpi.py")
    
# End of __main__ Code
#======================================================================

# init()
# ff = getMag()
# print(ff )




