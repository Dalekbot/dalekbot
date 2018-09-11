#!/usr/bin/env python

import RPi.GPIO as GPIO
import time   
GPIO.setmode(GPIO.BOARD)

pinMotorBRSpeed = 19
pinMotorBRForwards = 21
pinMotorBRBackwards = 23

GPIO.setwarnings(False) 

GPIO.setup(pinMotorBRSpeed, GPIO.OUT)
GPIO.setup(pinMotorBRForwards, GPIO.OUT)
GPIO.setup(pinMotorBRBackwards, GPIO.OUT)



time.sleep(1)
print 'low'
GPIO.output(pinMotorBRSpeed, GPIO.HIGH)
GPIO.output(pinMotorBRForwards, GPIO.HIGH)
GPIO.output(pinMotorBRBackwards, GPIO.LOW)

# How many times to turn the pin on and off each second
print 'Set Frequency'
Frequency = 20
# How long the pin stays on each cycle, as a percent (here, it's 50%) - AKA Speed
print 'Set DutyCycle'	
DutyCycle = 50

print 'Set Stop'
Stop = 0

print 'Set the GPIO to software PWM at ' + str(Frequency) + ' Hertz - Motor FR'
pwmMotorBRSpeed = GPIO.PWM(pinMotorBRSpeed, Frequency)

print 'Start the software PWM with a duty cycle of 0 (i.e. not moving) - Moter FR'
pwmMotorBRSpeed.start(Stop)

print 'speed 10'

pwmMotorBRSpeed.ChangeDutyCycle(10)

time.sleep(1)

print 'speed 50'
pwmMotorBRSpeed.ChangeDutyCycle(50)
time.sleep(3)


print 'speed 30'
pwmMotorBRSpeed.ChangeDutyCycle(100)

time.sleep(2)
print 'stop'
pwmMotorBRSpeed.ChangeDutyCycle(Stop)
time.sleep(2)