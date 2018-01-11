#!/usr/bin/env python

import pygame
import time
import RPi.GPIO as GPIO

# Initialise the pygame library
pygame.init()

# Connect to the first JoyStick
j = pygame.joystick.Joystick(0)
j.init()

print ('Initialized Joystick : %s' % j.get_name())


buttons = j.get_numbuttons()
print( "Number of buttons: {}".format(buttons) )

done = False


while done == False:
    for event in pygame.event.get():
        # if event.type == pygame.QUIT:
        #     done =True
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
# try:
#   # Check for any queued events and then process each one
#    # This is the main loop
#     while True:
#        # Check for any queued events and then process each one
#         events = pygame.event.get()
#         for event in events:
#           UpdateMotors = 0

#           if event.type == pygame.JOYAXISMOTION:
#             if event.axis == 1:
#               print ("axis 1")
#               UpdateMotors = 1
#             elif event.axis == 3:
#               print('axis 3 : %s ' % event.value) 
#               UpdateMotors = 1




# except KeyboardInterrupt:
#     # Turn off the motors
# GPIO.output(STANDBY, False)