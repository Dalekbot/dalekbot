import RPi.GPIO as GPIO  # Import GPIO divers
import DalekV2DriveV2      # Import my 4 Motor controller
import time   

import curses

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

# Main Imports and setup constants
speed = 20               # 0 is stopped, 100 is fastest
rightspeed = 50          # 0 is stopped, 100 is fastest
leftspeed = 50           # 0 is stopped, 100 is fastest
maxspeed = 100           # Set full Power
minspeed = 0             # Set min power  
innerturnspeed = 40      # Speed for Inner Wheels in a turn
outerturnspeed = 80      # Speed for Outer Wheels in a turn
hRes = 640               # PiCam Horizontal Resolution
vRes = 480               # PiCam Virtical Resolution
camera = 0               # Create PiCamera Object
video_capture = 0        # Create WebCam Object
soundvolume = 100     
GPIO.setwarnings(False) 

DalekV2DriveV2.init() 

# DalekV2DriveV2.forward(10)

# time.sleep(2)
# DalekV2DriveV2.forward(20)

# time.sleep(2)
# DalekV2DriveV2.forward(30)

# time.sleep(1)

# DalekV2DriveV2.backward(15)
# time.sleep(3)
# DalekV2DriveV2.backward(10)
# time.sleep(3)
# DalekV2DriveV2.spinLeft(70)
# time.sleep(5)

# DalekV2DriveV2.spinRight(70)
# time.sleep(5)
try:
  while True:
    char = screen.getch()
    if char == ord('q'):
      break
    elif char == curses.KEY_UP:
      DalekV2DriveV2.forward(speed)
      # print "UP"
    elif char == curses.KEY_DOWN:
      DalekV2DriveV2.backward(speed)
      # print("DOWN")
    elif char == curses.KEY_RIGHT:
      DalekV2DriveV2.spinRight(speed*2)
      # print("RIGHT")
    elif char == curses.KEY_LEFT:
      DalekV2DriveV2.spinLeft(speed*2)
      print("LEFT")
    elif char == 10:
      DalekV2DriveV2.stop()
    elif char == ord('a'):
      speed +=10 
      print (speed)
    elif char == ord('z'):
      speed -=10 
      print (speed)

      
finally:
  curses.nocbreak(); screen.keypad(0); curses.echo()
  curses.endwin()









  DalekV2DriveV2.cleanup()




