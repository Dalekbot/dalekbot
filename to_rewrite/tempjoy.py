import struct
import os.path
import time
import DalekV2Drive
import DalekSpi 
import autoDrive
import RPi.GPIO as GPIO  # Import GPIO divers
from DalekDebug import DalekPrint, DalekDebugOn 

###
### SETUP
###

# Uncommenet if run directly
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 
DalekDebugOn()
speed = 40
# the '/dev/input/js0' file is in the sudo root of the file system.
# it only apears once the device has paired.
# use the setup guide from https://www.piborg.org/blog/rpi-ps3-help

# wait until the joystick is paired...
# def init():
fn = '/dev/input/js0'

DalekPrint("Testing for joystick: {}...".format(fn))

file_exists = False
while file_exists == False:
 
  file_exists = os.path.exists(fn)
  DalekPrint('joystick paired: {} '.format(os.path.exists(fn)))
  time.sleep(3)


jsdev = open(fn, 'rb')
DalekPrint('Joystick paired. Ok \n', "Prd")
    



# DalekV2Drive.init()  # setup in main
# speed = 50           # setup in main

# Ps3 controller settings.
# def use():

# we
jsdev = open("/dev/input/js0", 'rb')

joystickD_padCurrentButton = 0
ps3_ControllerMode=2

axisX = 0
axisY = 0
minusX= False
minusY=False

leftPaddle = 0
rightPaddle = 0


def paddleControl(aX, aY,minusX, minusY):
    

    v_speed =  aY
    alog1 = aX/10
    if alog1>0:
      v_speed2 = v_speed/alog1
    else:
      v_speed2=1
    
    v_speed_3= aY
    alog2 = aX/5
    if alog2 > 0:
      v_speed_3 = alog2
    else:
      v_speed_3=1
  
    DalekPrint( 'ax:{}  aY:{} v_speed{} v_speed2 {}' .format(aX,aY , v_speed, v_speed2) )

    DalekPrint('v_speed: %s' % v_speed )
   
   
    # Paddle moved center
    if aY == 0 and aX ==0:
      DalekV2Drive.stop()
      DalekPrint("Stop","STP")
    
    #-------------------------------------
    # up movements

    # Paddle moved up only
    elif minusY  and aX == 0: 
      DalekV2Drive.forward(v_speed)
      DalekPrint("forward - {}".format(v_speed), "FW")

    # turnForwardRight
    elif minusY and minusX:
      
      if aY >50:

        DalekV2Drive.paddleForward(v_speed2, v_speed)
        DalekPrint('paddleForward turn right', "PTR")
      else:
        # DalekV2Drive.turnForwardLeft(v_speed, v_speed_3)
        DalekV2Drive.paddleForward(v_speed_3, v_speed)
        DalekPrint('paddleForward turn right',"PTR")
    # turnForwardLeft
    elif minusY and minusX == False:
      
      if aY > 50:
        DalekV2Drive.paddleForward( v_speed, v_speed2)
        # DalekV2Drive.turnBackwardRight(v_speed_3,v_speed)
        DalekPrint('turn right',"TR")
      else:
        DalekV2Drive.paddleForward( v_speed, v_speed_3)
        # DalekV2Drive.turnForwardRight(v_speed_3,v_speed)

    #-------------------------------------
    # spin movements

    #spin Left
    elif aY==0 and minusX :
      DalekV2Drive.spinLeft(aX)
    
    #spin Right
    elif aY==0 and minusX == False :
      DalekV2Drive.spinRight(aX)
#-------------------------------------
# Down movements
    # Paddle moved down only
    elif minusY == False and aX == 0:
      DalekV2Drive.backward(v_speed)
      DalekPrint("backwards - {}".format(v_speed), "BW")

    # backwards right
    elif minusY== False and minusX == False:
      
      DalekV2Drive.paddleBackward( v_speed, v_speed2)
      DalekPrint('turn right', "TR")
    # backwards left 
    elif minusY== False and minusX == True:
     
      DalekV2Drive.paddleBackward( v_speed2, v_speed)
      DalekPrint('turn right', "TR") 
#=====================================================
    
def dPadPressed(value,number, _joystickD_padCurrentButton):
  DalekPrint( "value:{} number:{} currentButton:{} " .format(value,number, _joystickD_padCurrentButton ))
  
  if (value==0) and (number == _joystickD_padCurrentButton):
    DalekV2Drive.stop()
    DalekPrint('#Stop()',"STP")
  #Up button
  else:
    if number == 4:
      if value: # value is 1 for pressed 0 for released.
        DalekPrint('forward')
        DalekV2Drive.forward(speed)
  
    #Right button
    elif number == 5:
      if value:
        DalekPrint('\nRight spin')
        # DalekV2Drive.spinRight(speed)
        autoDrive.DalekTurn(45) 
    
    # Down button
    elif number == 6:
      if value:
        DalekPrint('\nBackwards')
        DalekV2Drive.backward(speed)
    
    # Left button
    elif number == 7: 
      if value:
        DalekPrint('Left spin')
        autoDrive.DalekTurn(-45) 

def tankMode( _leftPaddle, _rightPaddle):

  # this mag reading is just for debug at the moment
  mag =DalekSpi.getMag()
  DalekPrint("left: {}  Right: {} mag:{}".format(_leftPaddle,_rightPaddle ,mag))
  
  if (_leftPaddle == 0) and (_rightPaddle == 0):
    DalekV2Drive.stop()
  elif (_leftPaddle < 0) and (_rightPaddle < 0):
    DalekV2Drive.paddleForward(- _leftPaddle, - _rightPaddle)
    DalekPrint("forwards")
  elif (_leftPaddle > 0) and (_rightPaddle > 0):
    DalekV2Drive.paddleBackward( _leftPaddle, _rightPaddle)
    DalekPrint("Backwards")
  elif (_leftPaddle <= 0) and (_rightPaddle >= 0):
    DalekV2Drive.turnForwardRight(- _leftPaddle,  _rightPaddle)
    DalekPrint("spinright")
  elif (_leftPaddle >= 0) and (_rightPaddle <= 0):
    DalekV2Drive.turnForwardLeft(  _leftPaddle,- _rightPaddle)
    DalekPrint("spin left")


  
#============================
# Main loop
# this is where we read the data from the joystick file/device
#============================

while True:
  #read 8 bits from the event buffer.
  evbuf = jsdev.read(8)
  if evbuf:
      time, value, type, number = struct.unpack('IhBB', evbuf)
      
      #  Button pressed event
      if type & 0x01:
        
        # D-Pad pressed
        if (number >=4 ) and (number <= 7):
          dPadPressed(value,number,joystickD_padCurrentButton )
          
          #only change current button when it is pressed not released
          if value:
            joystickD_padCurrentButton = number
        
        elif number == 0:
          
          if value: # dont increment on release.
            if ps3_ControllerMode <= 2:
              ps3_ControllerMode += 1
            else :
              ps3_ControllerMode = 1
            DalekPrint("You are in Mode {}" .format(ps3_ControllerMode))
        
        # L2 button
        elif number == 8:
          if value:
            AutoDrive2.DalekTurn(-180)    
        
         # R2 button
        elif number == 9:
          if value:
            AutoDrive2.DalekTurn(180)

           # L1 button
        elif number == 10:
          if value:
            AutoDrive2.DalekTurn(-90)
        # R1 button
        elif number == 11:
          if value:
            AutoDrive2.DalekTurn(90)
        # circle button
        elif number == 13:
          if value:
            mag =DalekSpi.getMag()
            DalekPrint("mag:{}".format(mag))

        else :
          DalekPrint("you pressed {}" .format(number))

      # Axis movement event
      elif type & 0x02:
        #DalekPrint('number{}'.format(number))
        
        # Left Thumbstick x axis.
        #normal mode
        if ps3_ControllerMode ==1 :
          if number == 0:
             # paddle up is -100 
             # paddle right is 100 
             # paddle left is -100 
             # paddle down is 100 
            axisX = int(value / 327.67)
            if axisX < 0:
              axisX = -axisX
              minusX = True
            else:
              minusX = False
            paddleControl(axisX, axisY,minusX, minusY)
          
          # Left Thumbstick Y axis
          elif number == 1:
            axisY =int( value / 327.67)
            if axisY < 0:
              minusY = True
              axisY = -axisY
            else:   
              minusY = False
            paddleControl(axisX, axisY,minusX, minusY)
          
          # Right Thumbstick X Axis
          # elif number == 2:
          #   axisY =int( value / 655.4)
            
          #   DalekPrint("right X:{}".format(axisY))
          
          # Right Thumbstick Y Axis
          elif number == 3:
            
             axisY =int( value / 655.4)
             speed = 50 - axisY
             DalekPrint("right y:{}  speed: {} ".format(axisY , speed))
        
        #Tank mode
        elif ps3_ControllerMode == 2:
          
          if number == 1:
             #DalekPrint("left side {}  {} ".format(leftPaddle , rightPaddle))
           
             leftPaddle= int( value / 327.67)
             
             tankMode(leftPaddle , rightPaddle)
            
          
          elif number == 3:
            # DalekPrint("right side..")
            rightPaddle= int( value / 327.67)
            tankMode(leftPaddle , rightPaddle)
