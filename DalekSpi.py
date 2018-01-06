#!/usr/bin/python

import spidev
import time
from DalekDebug import DalekPrint

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
    DalekPrint("spi bus speed set to:{} spi mode {}" .format( spi.max_speed_hz, spi.mode))

def getSensorData(_sensorNumber):
    # global spi 
    dataToSend = [_sensorNumber, 200, 201, 255]
    try:
        
        receivedBytes = spi.xfer(dataToSend)
        sensorValue = (receivedBytes[2] << 8) + receivedBytes[3]
        return sensorValue
    except expression as identifier:
        DalekPrint("error geting data from Arduino via spi bus")

def getMag():
    return getSensorData(4)


def readDevice1Data():
#   global SpiSetup,spi
 
  # create the return data variable
  piSensors = {'frontPing': 0, 'rearPing': 0,
               'leftPing': 0, 'rightPing': 0, 'compass': 0}
  piSensors['frontPing'] = getSensorData(0)
  time.sleep(.00001)
  piSensors['rearPing'] = getSensorData(3)
  time.sleep(.00001)
  piSensors['leftPing'] = getSensorData(1)
  time.sleep(.00001)
  piSensors['rightPing'] = getSensorData(2)
  time.sleep(.00001)
  piSensors['compass'] = getSensorData(4)

  return piSensors

def test():
   T = time.time()
   data =readDevice1Data()
   T2 = time.time()
   
   DalekPrint( data) 
   DalekPrint("time taken {}" .format(T2 - T)) 


#======================================================================	   
    
if __name__ == "__main__":
    DalekPrint("\n\nThis file 'DalekSpi.py' cannot be run directly. It is intended to be imported\n\n")
else:
    DalekPrint("Importing DalekSpi.py")
    
# End of __main__ Code
#======================================================================

# init()
# ff = getMag()
# print(ff )




