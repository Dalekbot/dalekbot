import os.path
import struct
import time

import autoDrive
import DalekSpi
import DalekV2Drive
# import RPi.GPIO as GPIO  # Import GPIO divers
from DalekDebug import DalekDebugClear, DalekDebugOn, DalekPrint
from termcolor import colored

###
### SETUP 
###

# the '/dev/input/js0' file is in the sudo root of the file system.
# it only apears once the device has paired.
# use the setup guide from https://www.piborg.org/blog/rpi-ps3-help

# wait until the joystick is paired...
def init():
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
def use(_speed, _currentMission):
  
  # use a dictionary so it can be python 2/3  compatable rather than nonlocal in  python 3
  settings = { 'currentMission': _currentMission}
  # global currentMission
  
  speed = _speed # set in the calling file

  # this is the joystick file we stream data from.
  jsdev = open("/dev/input/js0", 'rb')

  joystickD_padCurrentButton = 0  # used for debounce of switches on dpad.
  
  # The Main Mode we are in
  # 1 Drive mode
  # 2 Challenge Select Mode
  # 3 Exterminate Mode
  ps3_ControllerMode=1            
  

  axisX = 0        # main  axis variables nomalized
  axisY = 0        # main  axis variables nomalized
  minusX= False    # used for nomalizing the data
  minusY=False     # used for nomalizing the data
  
  leftPaddle = 0   # raw axis data
  rightPaddle = 0  # raw axis data
  
  ###############################################
  ###  Main Paddle controls on ps3 controller  ##
  ###############################################
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
  
  def missionSelect(value):
    numberOfMissions = 7
    currentMission = settings['currentMission']
    
    if value == 0: #Up Button
      if currentMission > 1:
        currentMission -=1
      else:
        currentMission = numberOfMissions
    
    else:         #Down Button
      if numberOfMissions >= (currentMission + 1): # so we dont exceed max number of missions
        currentMission +=1
      else:
        currentMission = 1
 
    settings['currentMission'] = currentMission
    displaySelectedChallenge()



   

  ###########################################################
  ###  DPad Buttons on ps3 controller (Left hand buttons) ##
  ###########################################################
  
  def buttonDpadUp():
    if ps3_ControllerMode == 2: # 2 Mission Select Mode
      missionSelect(0) 
    else:
      DalekPrint('Forwards', "FW") 
      DalekV2Drive.forward(speed)

  def buttonDpadDown():
    if ps3_ControllerMode == 2: # 2 Mission Select Mode
      missionSelect(1)
    else:
      DalekPrint('Backwards', "BW")  
      DalekV2Drive.backward(speed)
    
    
  def buttonDpadRight():
    if ps3_ControllerMode != 2:
      DalekPrint('Spin Rigrt', "SR") 
      DalekV2Drive.spinRight(speed)


  def buttonDpadLeft():
    if ps3_ControllerMode != 2:
      DalekPrint('Spin Left', "SL") 
      DalekV2Drive.spinLeft(speed)

  
  def dPadPressed(value,number, _joystickD_padCurrentButton):
    if (value==0) and (number == _joystickD_padCurrentButton):
      DalekV2Drive.stop()
      if ps3_ControllerMode ==1:
        DalekPrint("Stop", "SP")
    #Up button
    else:
      if number == 4:
        if value: # value is 1 for pressed 0 for released.
          buttonDpadUp()
    
      #Right button
      elif number == 5:
        if value:
          buttonDpadRight()
      
      # Down button
      elif number == 6:
        if value:
          buttonDpadDown()
      
      # Left button
      elif number == 7: 
        if value:
          buttonDpadLeft()
  
  def tankMode( _leftPaddle, _rightPaddle):
  
    # this mag reading is just for debug at the moment
    # mag =DalekSpi.getMag()
    # DalekPrint("left: {}  Right: {} mag:{}".format(_leftPaddle,_rightPaddle ,mag))
    DalekPrint("left: {}  Right: {}".format(_leftPaddle,_rightPaddle ))
    
    if (_leftPaddle == 0) and (_rightPaddle == 0):
      DalekV2Drive.stop()
      DalekDebugClear()
    elif (_leftPaddle < 0) and (_rightPaddle < 0):
      DalekV2Drive.paddleForward(- _leftPaddle, - _rightPaddle)
      DalekPrint("forwards","Fw")
    elif (_leftPaddle > 0) and (_rightPaddle > 0):
      DalekV2Drive.paddleBackward( _leftPaddle, _rightPaddle)
      DalekPrint("Backwards", "Bw")
    elif (_leftPaddle <= 0) and (_rightPaddle >= 0):
      DalekV2Drive.turnForwardRight(- _leftPaddle,  _rightPaddle)
      DalekPrint("Spin Right", "SR")
    elif (_leftPaddle >= 0) and (_rightPaddle <= 0):
      DalekV2Drive.turnForwardLeft(  _leftPaddle,- _rightPaddle)
      DalekPrint("Spin Left", "SL")
    

  def displaySelectedChallenge():
    currentMission = settings['currentMission']
    os.system('clear')
    
    DalekPrint(colored("\n\n\n\n           Challenge Select \n", 'red'))
    if currentMission == 1:
      DalekPrint(colored("        >>> Obstacle Course <<<",'green'))
    else:
      DalekPrint("           Obstacle Course")
    if currentMission == 2:
      DalekPrint(colored("        >>> Straight-Line Speed Test <<<",'green'))
    else:
      DalekPrint("           Straight-Line Speed Test")
    if currentMission == 3:
      DalekPrint(colored("        >>> Minimal Maze <<<",'green'))
    else:
      DalekPrint("           Minimal Maze")
    if currentMission == 4:
      DalekPrint(colored("        >>> Somewhere Over The Rainbow <<<",'green'))
    else:
      DalekPrint("           Somewhere Over The Rainbow")
    if currentMission == 5:
      DalekPrint(colored("        >>> PiNoon <<<",'green'))
    else:
      DalekPrint("           PiNoon")
    if currentMission == 6:
      DalekPrint(colored("        >>> Duck Shoot <<<",'green'))
    else:
      DalekPrint("           Duck Shoot")
    if currentMission == 7:
      DalekPrint(colored("        >>> Slightly Deranged Golf <<<",'green'))
    else:
      DalekPrint("           Slightly Deranged Golf")
   

    DalekPrint(colored("\n           Use UP and DOWN D-Pad Then Select",'yellow'))

    if currentMission == 1:  ## output for onboard device
      DalekPrint("","OC")
    elif currentMission == 2: 
      DalekPrint("","StL")
    elif currentMission == 3: 
      DalekPrint("","MM")
    elif currentMission == 4: 
      DalekPrint("","OR")
    elif currentMission == 5: 
      DalekPrint("","PN")
    elif currentMission == 6: 
      DalekPrint("","DS")
    elif currentMission == 7: 
      DalekPrint("","DG")
   
    


    
     



  ###########################################################
  ###  Symbol Buttons on the Controller                    ##
  ###########################################################
  def buttonCircle():
    DalekPrint("Circle Button Pressed")
  def buttonSquare():
    DalekPrint("Exterminate...")
  def buttonTriangle():
    DalekPrint("Triangle Button Pressed")
  def buttonCross():
    DalekPrint("Cross Button Pressed")
  
  ###########################################################
  ###  Lower Butons on the Controller                      ##
  ###########################################################
  def buttonL1():
    DalekPrint("L1 Button Pressed", "L1")
   
  def buttonL2():
    DalekPrint("L2 Button Pressed" , "L2")

  def buttonR1():
    DalekPrint("R1 Button Pressed", "R1")
    
  def buttonR2():
    DalekPrint("R2 Button Pressed", "R2" )
  ###########################################################
  ###  Main Buttons on the Controller                      ## 
  ###########################################################



  def buttonSelect(_ps3_ControllerMode):
    if _ps3_ControllerMode == 2:
      currentMission = settings['currentMission']
      os.system('clear')
      if _ps3_ControllerMode == 2: # Challenge Select Mode
        if currentMission == 1:
          DalekPrint("You selected Obstacle Course", "OC")
        elif currentMission == 2:
          DalekPrint("You selected Straight-Line Speed Test", "StL")
        elif currentMission == 3:
          DalekPrint("You selected Minimal Maze", "MM")
        elif currentMission == 4:
          DalekPrint("You selected Somewhere Over The Rainbow", "OR")
        elif currentMission == 5:
          DalekPrint("You selected PiNoon", "PN")
        elif currentMission == 6:
          DalekPrint("You selected Duck Shoot", "DS")
        elif currentMission == 7:
          DalekPrint("You selected Slightly Deranged Golf", "DG")
        
        else:
          displaySelectedChallenge()      # nothing has been selected yet.
      DalekPrint("got here")
    return 1 # resets ps3_ControllerMode 
      
    
 
  def buttonStart():
    DalekPrint("Start Button Pressed")
  
  def buttonPS3(_ps3_ControllerMode):
   
     # # change the controller Mode.
    _ps3_ControllerMode  +=1 
 
    if _ps3_ControllerMode == 1:
      os.system('clear')
      DalekPrint("You are in Drive Mode" .format(_ps3_ControllerMode),"-D")

    elif _ps3_ControllerMode == 2:
      displaySelectedChallenge()

      
    elif _ps3_ControllerMode == 3:
      _ps3_ControllerMode = 0
      os.system('clear')
      DalekPrint("You are in Exterminate Mode" .format(_ps3_ControllerMode),"-E")

    return _ps3_ControllerMode

  ###########################################################
  ###  paddle Buttons on the Controller                    ##
  ###########################################################  
  def buttonLeftPaddle():
    DalekPrint("Left Paddle Button Pressed")

  def buttonRightPaddle():
    DalekPrint("Right Paddle Button Pressed")

  
  #####################################################################
  ###                            Main loop                           ##
  ###  this is where we read the data from the joystick file/device  ##
  #####################################################################
  
  while True:
    #read 8 bits from the event buffer.
    evbuf = jsdev.read(8)
    if evbuf:
        time, value, type, number = struct.unpack('IhBB', evbuf)
        
        #  Button pressed event
        if type & 0x01:
          ########################
          # D-Pad button pressed #
          ########################
          if (number >=4 ) and (number <= 7):
            dPadPressed(value,number,joystickD_padCurrentButton )
                      
            #only change current button when it is pressed not released
            if value:
              joystickD_padCurrentButton = number
          #########################
          # All buttons NOT D-pad #
          #########################

          # Select button
          elif number == 0:
            
            if value: # dont increment on release.
              ps3_ControllerMode = buttonSelect(ps3_ControllerMode)
              
           #  Right paddle button
          elif number == 1:
            if value:
              buttonRightPaddle()

          #  Left Paddle button
          elif number == 2:
            if value:
              buttonLeftPaddle()

          #  Start Paddle button
          elif number == 3:
            if value:
              buttonStart()

          # L2 button
          elif number == 8:
            if value:
              buttonL2()   
          
           # R2 button
          elif number == 9:
            if value:
              buttonR2()
  
          # L1 button
          elif number == 10:
            if value:
              buttonL1()
          # R1 button
          elif number == 11:
            if value:
              buttonR1()

          # triangle button
          elif number == 12:
            if value:
              buttonTriangle()

          # circle button
          elif number == 13:
            if value:
              buttonCircle()

          #  Cross button
          elif number == 15:
            if value:
              buttonSquare()
          
          #  Cross button
          elif number == 14:
            if value:
              buttonCross()

          #  PS3  button
          elif number == 16:
            if value:
              ps3_ControllerMode = buttonPS3(ps3_ControllerMode)

         
          else :
            DalekPrint("you pressed {}" .format(number))
  
        # Axis movement event
        elif type & 0x02:
          #DalekPrint('number{}'.format(number))
          
          
         
          
          #Tank mode
          if ps3_ControllerMode == 1:
            
            if number == 1:
               #DalekPrint("left side {}  {} ".format(leftPaddle , rightPaddle))
             
               leftPaddle= int( value / 327.67)
               
               tankMode(leftPaddle , rightPaddle)
              
            
            elif number == 3:
              # DalekPrint("right side..")
              rightPaddle= int( value / 327.67)
              tankMode(leftPaddle , rightPaddle)
  return speed
