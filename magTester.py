import time
import DalekV2DriveV2

import DalekSpi 
import RPi.GPIO as GPIO  # Import GPIO divers
GPIO.setwarnings(False)


DalekV2DriveV2.init()
speed = 50

DalekSpi.init()


## raise the bot off the wheels and see how the mag changes when this is run.
mySleepTime = 0.3
#this is the time in the middle that it sleeps for change this to see what works best for you.
# also do some tests with the DalekV2DriveV2 functions to see if they make any difference
# this might be the time it takes to refresh the value on the Arduino 



greatestMag=0
mag = DalekSpi.getMag()
print("\n#################\n\ninitial value:{}" .format(mag))

speed =0

def speedtest():
  global speed, greatestMag
  DalekV2DriveV2.turnForwardRight(speed,speed)
  time.sleep(0.5)
  speed +=10
  mag = DalekSpi.getMag()
  if mag >greatestMag:
    greatestMag = mag
  print("\nmag:{}   Speed:{}" .format(mag,speed))
  return speed, greatestMag


def speedtest2():
  global speed, greatestMag
  DalekV2DriveV2.turnForwardLeft(speed,speed)
  time.sleep(0.5)
  speed -=10
  mag = DalekSpi.getMag()
  if mag >greatestMag:
    greatestMag = mag
  print("\nmag:{}   Speed:{}" .format(mag,speed))
  return speed, greatestMag

while speed < 100:
  speed, greatestMag = speedtest()


## the test to see how long the mag takes to recover.
print("### \nmag:{}   Speed:{}" .format(DalekSpi.getMag(),speed))
DalekV2DriveV2.stop()
time.sleep(mySleepTime)
print("### mag:{}   Speed:{}" .format(DalekSpi.getMag(),speed))
speed = 100




while speed > 0:
  speed, greatestMag = speedtest2()

print("\nmag:{}   Speed:{}" .format(DalekSpi.getMag(),speed))
DalekV2DriveV2.stop()
time.sleep(0.5)
print("\nEND mag:{}  Greatest mag:{}" .format(DalekSpi.getMag(),greatestMag))



