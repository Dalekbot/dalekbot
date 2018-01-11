import RPi.GPIO as GPIO  # Import GPIO divers
import dalek_drive      # Import my 4 Motor controller
import time   
import dalek_spi 
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
vRes = 480               # PiCam Vertical Resolution
camera = 0               # Create PiCamera Object
video_capture = 0        # Create WebCam Object
soundvolume = 100     
GPIO.setwarnings(False) 

dalek_drive.init()     
dalek_spi.init()
# dalek_drive.forward(10)

# time.sleep(2)
# dalek_drive.forward(20)

# time.sleep(2)
# dalek_drive.forward(30)

# time.sleep(1)

# dalek_drive.backward(15)
# time.sleep(3)
# dalek_drive.backward(10)
# time.sleep(3)
# dalek_drive.spinLeft(70)
# time.sleep(5)

# dalek_drive.spinRight(70)
# time.sleep(5)
try:
  while True:
    char = screen.getch()
    if char == ord('q'):
      break
    elif char == curses.KEY_UP:
      # dalek_drive.forward(speed)
      # print "UP"
      mag = dalek_spi.getMag()
      print("Mag:{}\n".format(mag))

    elif char == curses.KEY_DOWN:
      # dalek_drive.backward(speed)
      print("DOWN")

    elif char == curses.KEY_RIGHT:
      # dalek_drive.spinRight(speed*2)
      print("RIGHT")
    elif char == curses.KEY_LEFT:
      # dalek_drive.spinLeft(speed*2)
      print("LEFT")
    elif char == 10:
      dalek_drive.stop()
    elif char == ord('a'):
      speed +=10 
      print (speed)
    elif char == ord('z'):
      speed -=10 
      print (speed)

      
finally:
  curses.nocbreak(); screen.keypad(0); curses.echo()
  curses.endwin()









  dalek_drive.cleanup()




