# This is an abstraction layer for our debuging
# You can use the bash output window or plugin your own device.

import scrollphat 
import time

dalekDebugOn = False
DalekDebugOutputDevice = 0

# sets the output device 
# default is stout/command line only
# scollphat adds the bots display as well as stout
def DalekDebugSetOutputDevice(_dalekDebugOutputDevice):
  global DalekDebugOutputDevice

  if _dalekDebugOutputDevice == "scrollphat":
    
    scrollphat.clear()
    scrollphat.write_string("BOT")
    DalekDebugOutputDevice = 1
    dalekDebugOn = True # assume that as it is set,  use it.
  else:
    DalekDebugOutputDevice = 0

def DalekDebugOn():
  global dalekDebugOn
  dalekDebugOn = True

def DalekDebugOff():  
  global dalekDebugOn
  dalekDebugOn = False
# the text is the main bash output
# the code is the output to the bots screen
def DalekPrint(text, code=None):
 
  if dalekDebugOn:
    if DalekDebugOutputDevice == 0:
      print(text)
    elif DalekDebugOutputDevice == 1:
      #scrollphat
      print(text)
      if code != None:
        scrollphat.clear()
        scrollphat.write_string(code)
      pass

def DalekDebugClear(timeToPause=None):
  if DalekDebugOutputDevice == 1: # using the scrollphat
    scrollphat.clear()
  if timeToPause != None:
    time.sleep(timeToPause)

def DalekDebugSetBrightness(valueInt):
  if DalekDebugOutputDevice == 1: # using the scrollphat
    scrollphat.set_brightness(valueInt)
  

def DalekDebugDestroy():
  DalekDebugClear()



  # print("hello:{}".format(DalekDebugOn))


if __name__ == "__main__":
    print("\n\nDalekDebug.py cannot be run directly. It is intended to be imported\n\n")
else:
    print("Importing DalekDebug.py")