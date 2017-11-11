import smbus
import time
from enum import Enum

bus = smbus.SMBus(1)

#this is the address of the arduino
address = 0x04


class i2cMode(Enum):
  ALL = 1
  ULTRASONIC = 2

#set default mode to receive all
currenti2cMode = i2cMode.ALL

def writeNumber(value):
    bus.write_byte(address,value)

def readNumber():
  number = bus.read_byte(address)
  return number

#Set the mode on the slave device.
def setMode(i2cmode):
  if currenti2cMode != i2cmode:
    writeNumber(i2cmode)
    time.sleep(.5)


while True:
  var =int(input("Enter a number between 1 and 9"))
  if not var:
    continue
  if var == 5:
    #start timer
    timestart = time.time()
   
    setMode(i2cMode.ALL)
    
    left = readNumber()

    
    forward = readNumber()

    
    right = readNumber()

    
    behind = readNumber()

    #calculate the time it takes to get all data.
    taken = time.time() - timestart
    print ("data back in {} seconds.  Data:(Forward: {},Right: {},Behind: {},Left: {})".format(taken,left,forward, right, behind))
 
    # timeent= time.time()
    # taken = timeent - timestart
    # print ("Arduino, hey  RPI, i received a digit: {} in {} seconds").format(number,taken)
  else:
    



    writeNumber(var)
    print("RPI: hi Arduino, I sent you a digit {}".format(var))
    
  
    time.sleep(1)
  
    number = readNumber()
    print ("Arduino, hey  RPI, i received a digit: {} in ".format(number))