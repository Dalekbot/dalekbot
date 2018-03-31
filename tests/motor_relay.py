import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import time
from dalek import drive 
import RPi.GPIO as GPIO 
# pinMotorBRSpeed = 11
# pinMotorBRForwards = 13
# pinMotorBRBackwards = 15

# pinMotorBRSpeed = 33
# pinMotorBRForwards = 35
# pinMotorBRBackwards = 37

# pinMotorBRSpeed = 36
# pinMotorBRForwards = 38
# pinMotorBRBackwards = 40

# pinMotorBRSpeed = 8
# pinMotorBRForwards = 12
# pinMotorBRBackwards = 10

# pin_motor_relay = 31

# Speed = 50
# Frequency = 100
# DutyCycle = 50
# Stop = 0
#####################
## SETUP
#####################
GPIO.setwarnings(False)
drive.init()
# GPIO.setmode(GPIO.BOARD)

# # turn on the relay
# GPIO.setup(pin_motor_relay,GPIO.OUT)
# GPIO.output(pin_motor_relay, GPIO.HIGH)


# GPIO.setup(pinMotorBRSpeed, GPIO.OUT)
# GPIO.setup(pinMotorBRForwards, GPIO.OUT)
# GPIO.setup(pinMotorBRBackwards, GPIO.OUT)

# pwmMotorBRSpeed = GPIO.PWM(pinMotorBRSpeed, Frequency)
# pwmMotorBRSpeed.start(Stop)

#######################
### main
#######################


while True:
    # toggle the Back right motor
    # GPIO.output(pin_motor_relay, GPIO.HIGH)
    # time.sleep(1)
    # print("on")
    # GPIO.output(pin_motor_relay, GPIO.LOW)
    # time.sleep(1)
    # print("off")
    # pwmMotorBRSpeed.ChangeDutyCycle(Speed)
    # GPIO.output(pinMotorBRForwards, GPIO.HIGH)
    # GPIO.output(pinMotorBRBackwards, GPIO.LOW)
    drive.forward(30)
    time.sleep(2)
    drive.backward(30)
    time.sleep(2)
    drive.spinLeft(50)
    time.sleep(2)
    drive.spinRight(50)
    time.sleep(2)