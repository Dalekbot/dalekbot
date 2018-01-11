#!/usr/bin/env python
import os.path
import struct
import time
import dalek_drive
from dalek_debug import DalekDebugClear, DalekDebugOn, DalekPrint
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
    
# Ps3 controller settings.
def use(speed, dalek_sounds):

  dalek_sounds = dalek_sounds

  current_challenge = 1
  speed = speed # set in the calling file

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
  
  
  def challenge_select(value):
    nonlocal current_challenge
    numberOfMissions = 7
    currentChallenge = current_challenge
    
    if value == 0: #Up Button
      if currentChallenge > 1:
        currentChallenge -=1
      else:
        currentChallenge = numberOfMissions
    
    else:         #Down Button
      if numberOfMissions >= (currentChallenge + 1): # so we dont exceed max number of missions
        currentChallenge +=1
      else:
        currentChallenge = 1
 
    current_challenge = currentChallenge
    display_selected_challenge()

  ###########################################################
  ###  DPad Buttons on ps3 controller (Left hand buttons) ##
  ###########################################################
  
  def dpad_up_button_pressed():
    if ps3_ControllerMode == 2: # 2 Mission Select Mode
      challenge_select(0) 
    else:
      DalekPrint('Forwards', "FW") 
      dalek_drive.forward(speed)

  def dpad_down_button_pressed():
    if ps3_ControllerMode == 2: # 2 Mission Select Mode
      challenge_select(1)
    else:
      DalekPrint('Backwards', "BW")  
      dalek_drive.backward(speed)
    
    
  def dpad_right_button_pressed():
    if ps3_ControllerMode != 2:
      DalekPrint('Spin Rigrt', "SR") 
      dalek_drive.spinRight(speed)


  def dpad_left_button_pressed():
    if ps3_ControllerMode != 2:
      DalekPrint('Spin Left', "SL") 
      dalek_drive.spinLeft(speed)

  
  def dpad_button_pressed(value,number, _joystickD_padCurrentButton):
    if (value==0) and (number == _joystickD_padCurrentButton):
      dalek_drive.stop()
      if ps3_ControllerMode ==1:
        DalekPrint("Stop", "SP")
    #Up button
    else:
      if number == 4:
        if value: # value is 1 for pressed 0 for released.
          dpad_up_button_pressed()
    
      #Right button
      elif number == 5:
        if value:
          dpad_right_button_pressed()
      
      # Down button
      elif number == 6:
        if value:
          dpad_down_button_pressed()
      
      # Left button
      elif number == 7: 
        if value:
          dpad_left_button_pressed()
  
  def tank_drive_mode( _leftPaddle, _rightPaddle):
    DalekPrint("left: {}  Right: {}".format(_leftPaddle,_rightPaddle ))
    
    if (_leftPaddle == 0) and (_rightPaddle == 0):
      dalek_drive.stop()
      DalekDebugClear()
    elif (_leftPaddle < 0) and (_rightPaddle < 0):
      dalek_drive.paddleForward(- _leftPaddle, - _rightPaddle)
      DalekPrint("forwards","Fw")
    elif (_leftPaddle > 0) and (_rightPaddle > 0):
      dalek_drive.paddleBackward( _leftPaddle, _rightPaddle)
      DalekPrint("Backwards", "Bw")
    elif (_leftPaddle <= 0) and (_rightPaddle >= 0):
      dalek_drive.turnForwardRight(- _leftPaddle,  _rightPaddle)
      DalekPrint("Spin Right", "SR")
    elif (_leftPaddle >= 0) and (_rightPaddle <= 0):
      dalek_drive.turnForwardLeft(  _leftPaddle,- _rightPaddle)
      DalekPrint("Spin Left", "SL")
    

  def display_selected_challenge():
    # Prints out the Challenge menu
    # It is preformated.
    currentChallenge = current_challenge
    os.system('clear')
    
    DalekPrint(colored("\n\n\n\n           Challenge Select \n", 'red'))
    if currentChallenge == 1:
      DalekPrint(colored("        >>> Obstacle Course <<<",'green'))
    else:
      DalekPrint("           Obstacle Course")
    if currentChallenge == 2:
      DalekPrint(colored("        >>> Straight-Line Speed Test <<<",'green'))
    else:
      DalekPrint("           Straight-Line Speed Test")
    if currentChallenge == 3:
      DalekPrint(colored("        >>> Minimal Maze <<<",'green'))
    else:
      DalekPrint("           Minimal Maze")
    if currentChallenge == 4:
      DalekPrint(colored("        >>> Somewhere Over The Rainbow <<<",'green'))
    else:
      DalekPrint("           Somewhere Over The Rainbow")
    if currentChallenge == 5:
      DalekPrint(colored("        >>> PiNoon <<<",'green'))
    else:
      DalekPrint("           PiNoon")
    if currentChallenge == 6:
      DalekPrint(colored("        >>> Duck Shoot <<<",'green'))
    else:
      DalekPrint("           Duck Shoot")
    if currentChallenge == 7:
      DalekPrint(colored("        >>> Slightly Deranged Golf <<<",'green'))
    else:
      DalekPrint("           Slightly Deranged Golf")
   

    DalekPrint(colored("\n           Use UP and DOWN D-Pad Then Select",'yellow'))

    if currentChallenge == 1:  ## output for onboard device
      DalekPrint("","OC")
    elif currentChallenge == 2: 
      DalekPrint("","StL")
    elif currentChallenge == 3: 
      DalekPrint("","MM")
    elif currentChallenge == 4: 
      DalekPrint("","OR")
    elif currentChallenge == 5: 
      DalekPrint("","PN")
    elif currentChallenge == 6: 
      DalekPrint("","DS")
    elif currentChallenge == 7: 
      DalekPrint("","DG")

  ###########################################################
  ###  Symbol Buttons on the Controller                    ##
  ###########################################################
  def button_circle():
    dalek_sounds.play_sound("Must Survive")
    DalekPrint("Circle Button Pressed")
  def button_square():
    dalek_sounds.play_sound("exterminate")
    DalekPrint("Exterminate...")
  def button_triangle():
    dalek_sounds.play_sound("Stay")
    DalekPrint("Triangle Button Pressed")
  def button_cross():
    dalek_sounds.play_sound("Time is right")
    DalekPrint("Cross Button Pressed")
  
  ###########################################################
  ###  Lower Butons on the Controller                      ##
  ###########################################################
  def button_L1():
    DalekPrint("L1 Button Pressed", "L1")
   
  def button_L2():
    dalek_sounds.decreese_volume_level()
    DalekPrint("L2 Button Pressed" , "L2")

  def button_R1():
    DalekPrint("R1 Button Pressed", "R1")
    
  def button_R2():
    dalek_sounds.increese_volume_level()
    DalekPrint("R2 Button Pressed", "R2" )
  ###########################################################
  ###  Main Buttons on the Controller                      ## 
  ###########################################################

  def button_select(_ps3_ControllerMode):
    if _ps3_ControllerMode == 2:
      currentChallenge = current_challenge
      os.system('clear')
      if _ps3_ControllerMode == 2: # Challenge Select Mode
        if currentChallenge == 1:
          DalekPrint("You selected Obstacle Course", "OC")
        elif currentChallenge == 2:
          DalekPrint("You selected Straight-Line Speed Test", "StL")
        elif currentChallenge == 3:
          DalekPrint("You selected Minimal Maze", "MM")
        elif currentChallenge == 4:
          DalekPrint("You selected Somewhere Over The Rainbow", "OR")
        elif currentChallenge == 5:
          DalekPrint("You selected PiNoon", "PN")
        elif currentChallenge == 6:
          DalekPrint("You selected Duck Shoot", "DS")
        elif currentChallenge == 7:
          DalekPrint("You selected Slightly Deranged Golf", "DG")
        
        else:
          display_selected_challenge()      # nothing has been selected yet.
  
    return 1 # resets ps3_ControllerMode  to Drive Mode
      
 
  def button_start():
    DalekPrint("Start Button Pressed")
  
  def button_PS3(_ps3_ControllerMode):
   
     # # change the controller Mode.
    _ps3_ControllerMode  +=1 
 
    if _ps3_ControllerMode == 1:
      os.system('clear')
      DalekPrint("You are in Drive Mode" .format(_ps3_ControllerMode),"-D")

    elif _ps3_ControllerMode == 2:
      display_selected_challenge()

      
    elif _ps3_ControllerMode == 3:
      _ps3_ControllerMode = 0
      os.system('clear')
      DalekPrint("You are in Exterminate Mode" .format(_ps3_ControllerMode),"-E")

    return _ps3_ControllerMode

  ###########################################################
  ###  paddle Buttons on the Controller                    ##
  ###########################################################  
  def button_left_paddle():
    DalekPrint("Left Paddle Button Pressed")

  def button_right_paddle():
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
            dpad_button_pressed(value,number,joystickD_padCurrentButton )
                      
            #only change current button when it is pressed not released
            if value:
              joystickD_padCurrentButton = number
          #########################
          # All buttons NOT D-pad #
          #########################

          # Select button
          elif number == 0:
            
            if value: # dont increment on release.
              ps3_ControllerMode = button_select(ps3_ControllerMode)
              
           #  Right paddle button
          elif number == 1:
            if value:
              button_right_paddle()

          #  Left Paddle button
          elif number == 2:
            if value:
              button_left_paddle()

          #  Start Paddle button
          elif number == 3:
            if value:
              button_start()

          # L2 button
          elif number == 8:
            if value:
              button_L2()   
          
           # R2 button
          elif number == 9:
            if value:
              button_R2()
  
          # L1 button
          elif number == 10:
            if value:
              button_L1()
          # R1 button
          elif number == 11:
            if value:
              button_R1()

          # triangle button
          elif number == 12:
            if value:
              button_triangle()

          # circle button
          elif number == 13:
            if value:
              button_circle()

          #  Cross button
          elif number == 15:
            if value:
              button_square()
          
          #  Cross button
          elif number == 14:
            if value:
              button_cross()

          #  PS3  button
          elif number == 16:
            if value:
              ps3_ControllerMode = button_PS3(ps3_ControllerMode)
 
         
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
               
               tank_drive_mode(leftPaddle , rightPaddle)
              
            
            elif number == 3:
              # DalekPrint("right side..")
              rightPaddle= int( value / 327.67)
              tank_drive_mode(leftPaddle , rightPaddle)
  return speed
 

def main():
  pass

  # import RPi.GPIO as GPIO 
  # dalek_drive.init()
  # GPIO.setmode(GPIO.BOARD)   # Set the GPIO pins as numbering - Also set in dalek_drive.py
  # GPIO.setwarnings(False)    # Turn GPIO warnings off - CAN ALSO BE Set in dalek_drive.py
  # init()
  # use(50)

if __name__ == '__main__':
    import time 
    main()