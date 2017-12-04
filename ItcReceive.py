#!/usr/bin/env python

import smbus
import time
bus = smbus.SMBus(1)

#this module just receives data sent from the remote device.


#this is the address of the Arduino
address = 0x05