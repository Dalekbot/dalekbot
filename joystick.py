import struct
import os.path
import time
import DalekV2DriveV2
import DalekSpi 
import autoDrive
import RPi.GPIO as GPIO  # Import GPIO divers

###
### SETUP
###

GPIO.setwarnings(False) 

# the '/dev/input/js0' file is in the sudo root of the file system.
# it only apears once the device has paired.
# use the setup guide from https://www.piborg.org/blog/rpi-ps3-help

# wait until the joystick is paired...
fn = '/dev/input/js0'
print('Testing for joystick: %s...' % fn)

file_exists = False
while file_exists == False:
 
  file_exists = os.path.exists(fn)
  print ('joystick paired: {} '.format(os.path.exists(fn)))
  time.sleep(3)


jsdev = open(fn, 'rb')
print ('Joystick paired. Ok \n')



DalekV2DriveV2.init()  
speed = 50

# Ps3 controller settings.
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
  
    print ( 'ax:{}  aY:{} v_speed{} v_speed2 {}' .format(aX,aY , v_speed, v_speed2) )

    print ('v_speed: %s' % v_speed )
   
   
    # Paddle moved center
    if aY == 0 and aX ==0:
      DalekV2DriveV2.stop()
      print ('stop')
    
    #-------------------------------------
    # up movements

    # Paddle moved up only
    elif minusY  and aX == 0: 
      DalekV2DriveV2.forward(v_speed)
      print ('forward')

    # turnForwardRight
    elif minusY and minusX:
      
      if aY >50:

        DalekV2DriveV2.paddleForward(v_speed2, v_speed)
        # DalekV2DriveV2.turnForwardRight(v_speed,v_speed_3)
        print ('paddleForward turn right')
      else:
        # DalekV2DriveV2.turnForwardLeft(v_speed, v_speed_3)
        DalekV2DriveV2.paddleForward(v_speed_3, v_speed)
        print ('paddleForward turn right')
    # turnForwardLeft
    elif minusY and minusX == False:
      
      if aY > 50:
        DalekV2DriveV2.paddleForward( v_speed, v_speed2)
        # DalekV2DriveV2.turnBackwardRight(v_speed_3,v_speed)
        print ('turn right')
      else:
        DalekV2DriveV2.paddleForward( v_speed, v_speed_3)
        # DalekV2DriveV2.turnForwardRight(v_speed_3,v_speed)

    #-------------------------------------
    # spin movements

    #spin Left
    elif aY==0 and minusX :
      DalekV2DriveV2.spinLeft(aX)
    
    #spin Right
    elif aY==0 and minusX == False :
      DalekV2DriveV2.spinRight(aX)
#-------------------------------------
# Down movements
    # Paddle moved down only
    elif minusY == False and aX == 0:
      DalekV2DriveV2.backward(v_speed)
      print ('backwards')

    # backwards right
    elif minusY== False and minusX == False:
      
      DalekV2DriveV2.paddleBackward( v_speed, v_speed2)
      print ('turn right')
    # backwards left 
    elif minusY== False and minusX == True:
     
      DalekV2DriveV2.paddleBackward( v_speed2, v_speed)
      print ('turn right') 
#=====================================================
    
def dPadPressed(value,number, _joystickD_padCurrentButton):
  print( "value:{} number:{} currentButton:{} " .format(value,number, _joystickD_padCurrentButton ))
  
  if (value==0) and (number == _joystickD_padCurrentButton):
    DalekV2DriveV2.stop()
    print('#Stop()')
  #Up button
  else:
    if number == 4:
      if value: # value is 1 for pressed 0 for released.
        print('forward')
        DalekV2DriveV2.forward(speed)
  
    #Right button
    elif number == 5:
      if value:
        print('\nRight spin')
        # DalekV2DriveV2.spinRight(speed)
        autoDrive.DalekTurn(45) 
    
    # Down button
    elif number == 6:
      if value:
        print('\nBackwards')
        DalekV2DriveV2.backward(speed)
    
    # Left button
    elif number == 7: 
      if value:
        print('Left spin')
        autoDrive.DalekTurn(-45) 

def tankMode( _leftPaddle, _rightPaddle):

  # this mag reading is just for debug at the moment
  mag =DalekSpi.getMag()
  print("left: {}  Right: {} mag:{}".format(_leftPaddle,_rightPaddle ,mag))
  
  if (_leftPaddle == 0) and (_rightPaddle == 0):
    DalekV2DriveV2.stop()
  elif (_leftPaddle < 0) and (_rightPaddle < 0):
    DalekV2DriveV2.paddleForward(- _leftPaddle, - _rightPaddle)
    print("forwards")
  elif (_leftPaddle > 0) and (_rightPaddle > 0):
    DalekV2DriveV2.paddleBackward( _leftPaddle, _rightPaddle)
    print("Backwards")
  elif (_leftPaddle <= 0) and (_rightPaddle >= 0):
    DalekV2DriveV2.turnForwardRight(- _leftPaddle,  _rightPaddle)
    print("spinright")
  elif (_leftPaddle >= 0) and (_rightPaddle <= 0):
    DalekV2DriveV2.turnForwardLeft(  _leftPaddle,- _rightPaddle)
    print("spin left")


  
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
            print("You are in Mode {}" .format(ps3_ControllerMode))
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
            print("mag:{}".format(mag))

        else :
          print("you pressed {}" .format(number))

      # Axis movement event
      elif type & 0x02:
        #print('number{}'.format(number))
        
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
            
          #   print("right X:{}".format(axisY))
          
          # Right Thumbstick Y Axis
          elif number == 3:
            
             axisY =int( value / 655.4)
             speed = 50 - axisY
             print("right y:{}  speed: {} ".format(axisY , speed))
        
        #Tank mode
        elif ps3_ControllerMode == 2:
          
          if number == 1:
             #print("left side {}  {} ".format(leftPaddle , rightPaddle))
           
             leftPaddle= int( value / 327.67)
             
             tankMode(leftPaddle , rightPaddle)
            
          
          elif number == 3:
            # print("right side..")
            rightPaddle= int( value / 327.67)
            tankMode(leftPaddle , rightPaddle)
