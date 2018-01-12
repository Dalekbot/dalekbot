#!/usr/bin/env python
import os.path
import struct
import time
from dalek import drive 
from dalek import debug
from dalek import ui

###
### SETUP 
###

# the '/dev/input/js0' file is in the sudo root of the file system.
# it only apears once the device has paired.
# use the setup guide from https://www.piborg.org/blog/rpi-ps3-help

# wait until the joystick is paired...
def init():
    fn = '/dev/input/js0'
    
    debug.print_to_all_devices("Testing for joystick: {}...".format(fn))
    
    file_exists = False
    while file_exists == False:
     
      file_exists = os.path.exists(fn)
      debug.print_to_all_devices('joystick paired: {} '.format(os.path.exists(fn)))
      time.sleep(3)
    
    
    jsdev = open(fn, 'rb')
    debug.print_to_all_devices('Joystick paired. Ok \n', "Prd")
    
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
    ui.display_selected_challenge(current_challenge)

  ###########################################################
  ###  DPad Buttons on ps3 controller (Left hand buttons) ##
  ###########################################################
  
  def dpad_up_button_pressed():
    if ps3_ControllerMode == 2: # 2 Mission Select Mode
      challenge_select(0) 
    else:
      debug.print_to_all_devices('Forwards', "FW") 
      drive.forward(speed)

  def dpad_down_button_pressed():
    if ps3_ControllerMode == 2: # 2 Mission Select Mode
      challenge_select(1)
    else:
      debug.print_to_all_devices('Backwards', "BW")  
      drive.backward(speed)
    
    
  def dpad_right_button_pressed():
    if ps3_ControllerMode != 2:
      debug.print_to_all_devices('Spin Rigrt', "SR") 
      drive.spinRight(speed)


  def dpad_left_button_pressed():
    if ps3_ControllerMode != 2:
      debug.print_to_all_devices('Spin Left', "SL") 
      drive.spinLeft(speed)

  
  def dpad_button_pressed(value,number, _joystickD_padCurrentButton):
    if (value==0) and (number == _joystickD_padCurrentButton):
      drive.stop()
      if ps3_ControllerMode ==1:
        debug.print_to_all_devices("Stop", "SP")
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
    debug.print_to_all_devices("left: {}  Right: {}".format(_leftPaddle,_rightPaddle ))
    
    if (_leftPaddle == 0) and (_rightPaddle == 0):
      drive.stop()
      debug.clear()
    elif (_leftPaddle < 0) and (_rightPaddle < 0):
      drive.paddleForward(- _leftPaddle, - _rightPaddle)
      debug.print_to_all_devices("forwards","Fw")
    elif (_leftPaddle > 0) and (_rightPaddle > 0):
      drive.paddleBackward( _leftPaddle, _rightPaddle)
      debug.print_to_all_devices("Backwards", "Bw")
    elif (_leftPaddle <= 0) and (_rightPaddle >= 0):
      drive.turnForwardRight(- _leftPaddle,  _rightPaddle)
      debug.print_to_all_devices("Spin Right", "SR")
    elif (_leftPaddle >= 0) and (_rightPaddle <= 0):
      drive.turnForwardLeft(  _leftPaddle,- _rightPaddle)
      debug.print_to_all_devices("Spin Left", "SL")

  ###########################################################
  ###  Symbol Buttons on the Controller                    ##
  ###########################################################
  def button_circle():
    dalek_sounds.play_sound("Must Survive")
    debug.print_to_all_devices("Circle Button Pressed")
  def button_square():
    dalek_sounds.play_sound("exterminate")
    debug.print_to_all_devices("Exterminate...")
  def button_triangle():
    dalek_sounds.play_sound("Stay")
    debug.print_to_all_devices("Triangle Button Pressed")
  def button_cross():
    dalek_sounds.play_sound("Time is right")
    debug.print_to_all_devices("Cross Button Pressed")
  
  ###########################################################
  ###  Lower Butons on the Controller                      ##
  ###########################################################
  def button_L1():
    debug.print_to_all_devices("L1 Button Pressed", "L1")
   
  def button_L2():
    dalek_sounds.decreese_volume_level()
    debug.print_to_all_devices("L2 Button Pressed" , "L2")

  def button_R1():
    debug.print_to_all_devices("R1 Button Pressed", "R1")
    
  def button_R2():
    dalek_sounds.increese_volume_level()
    debug.print_to_all_devices("R2 Button Pressed", "R2" )
  ###########################################################
  ###  Main Buttons on the Controller                      ## 
  ###########################################################

  def button_select(ps3_controller_mode):
    if ps3_controller_mode == 2:
      os.system('clear')
      if ps3_controller_mode == 2: # Challenge Select Mode
          ui.you_selected_challenge(current_challenge)
             # nothing has been selected yet.
  
    return 1 # resets ps3_ControllerMode  to Drive Mode
      
 
  def button_start():
    debug.print_to_all_devices("Start Button Pressed")
  
  def button_PS3(_ps3_ControllerMode):
   
     # # change the controller Mode.
    _ps3_ControllerMode  +=1 
 
    if _ps3_ControllerMode == 1:
      os.system('clear')
      debug.print_to_all_devices("You are in Drive Mode" .format(_ps3_ControllerMode),"-D")

    elif _ps3_ControllerMode == 2:
      ui.display_selected_challenge(current_challenge)

      
    elif _ps3_ControllerMode == 3:
      _ps3_ControllerMode = 0
      os.system('clear')
      debug.print_to_all_devices("You are in Exterminate Mode" .format(_ps3_ControllerMode),"-E")

    return _ps3_ControllerMode

  ###########################################################
  ###  paddle Buttons on the Controller                    ##
  ###########################################################  
  def button_left_paddle():
    debug.print_to_all_devices("Left Paddle Button Pressed")

  def button_right_paddle():
    debug.print_to_all_devices("Right Paddle Button Pressed")

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
            debug.print_to_all_devices("you pressed {}" .format(number))
  
        # Axis movement event
        elif type & 0x02:
          #debug.print_to_all_devices('number{}'.format(number))
          
          
         
          
          #Tank mode
          if ps3_ControllerMode == 1:
            
            if number == 1:
               #debug.print_to_all_devices("left side {}  {} ".format(leftPaddle , rightPaddle))
             
               leftPaddle= int( value / 327.67)
               
               tank_drive_mode(leftPaddle , rightPaddle)
              
            
            elif number == 3:
              # debug.print_to_all_devices("right side..")
              rightPaddle= int( value / 327.67)
              tank_drive_mode(leftPaddle , rightPaddle)
  return speed
 

def main():
  pass


if __name__ == '__main__':
    import time 
    main()