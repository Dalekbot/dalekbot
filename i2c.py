#!/usr/bin/env python

import smbus
import time
bus = smbus.SMBus(1)

###
### this module should be imported 
### Set the i2cMode that best suits your task
### Switching i2cMode is takes time as you have to wait for the request response then request data 
###  it is better to get more data than required and throw it away. 
###

#this is the address of the Arduino
address = 0x05


class i2cMode(object):
  ALL = 1
  ULTRASONIC = 2
  MAGNETOMETER = 3

#set default mode to receive all
currentI2cMode = i2cMode.ALL

#TODO send sensor number then data from the arduino.
## at the moment you get  different results each time it boots
## check the arduino is working properly...
def init():
  currentI2cMode = i2cMode.ALL



def writeNumber(value): 
    bus.write_byte(address,value)

def readNumber():
  number = bus.read_byte(address)
  return number

#Set the mode on the slave device.
def setMode(i2cMode):
  if currentI2cMode != i2cMode:
    writeNumber(i2cMode)
    time.sleep(.5)

def getAll():
  global i2cMode,  currentI2cMode
  # timestart = time.time()
  if currentI2cMode != i2cMode.ALL:
    setMode(i2cMode.ALL)
    currentI2cMode = i2cMode.ALL
    
  right = readNumber()
  behind = readNumber()
  forward = readNumber()
  left = readNumber()
  #calculate the time it takes to get all data.
  # taken = time.time() - timestart
  print ("Data:(forwards: {},left: {},right: {},behind: {})".format(forward,left, right, behind))
    


while True:
  getAll()
  time.sleep(1) 

    
   