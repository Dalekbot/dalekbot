import struct
import os.path
import time
import DalekV2DriveV2
import RPi.GPIO as GPIO  # Import GPIO divers

###
### SETUP
###

GPIO.setwarnings(False) 


# wait until the joystick is paired...
fn = '/dev/input/js0'
print('Testing for joystick: %s...' % fn)

fexists = False
while fexists:
 
  fexists = os.path.isfile(fn)
  print ('joystick not paired.')
  time.sleep(3)


jsdev = open(fn, 'rb')
print ('Joystick paired. Ok \n')



DalekV2DriveV2.init() 
speed = 90

buttonPressed = 0
axisX = 0
axisY = 0
minusX= False
minusY=False



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
    
def dPadPressed(number): 



#============================
# Main loop
#============================

while True:
  #read 8 bits from the event buffer.
  evbuf = jsdev.read(8)
  if evbuf:
      time, value, type, number = struct.unpack('IhBB', evbuf)
      # if type & 0x80:
      #        print ("(initial)")
      if type & 0x01:
        
        #
        if number == 4:

          print ('button still pressed %s' % buttonPressed)
          if value:
            print('forward')
            DalekV2DriveV2.forward(speed)
            buttonPressed=4
          elif buttonPressed == 4:
            print('forward stop')
            DalekV2DriveV2.stop()
          # elif value == False & buttonStillPressed == False:


        elif number == 5:
          if value:
            print('Right spin')
            DalekV2DriveV2.spinRight(speed)
            buttonPressed = 5
          elif buttonPressed == 5:
            print('stop')
            DalekV2DriveV2.stop()

        elif number == 6:
          if value:
            print('Backwards')
            DalekV2DriveV2.backward(speed)
            buttonPressed = 6
          elif  buttonPressed == 6:
            print('stop')
            DalekV2DriveV2.stop()


        elif number == 7: 
          if value:
            print('Left spin')
            DalekV2DriveV2.spinLeft(speed)
            buttonPressed = 7
          elif  buttonPressed == 7:
            print('stop')
            DalekV2DriveV2.stop()

        # if value:
        #   print ('pressed')
        # else:
        #   print ('released')

      
      # paddle moved
      if type & 0x02:
        
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

        if number == 1:
          axisY =int( value / 327.67)
          if axisY < 0:
            minusY = True
            axisY = -axisY
          else:
            minusY = False
          paddleControl(axisX, axisY,minusX, minusY)
