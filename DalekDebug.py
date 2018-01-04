# This is an abstraction layer for our debuging
# You can use the bash output window or plugin your own device.



dalekDebugOn = False
DalekDebugOutputDevice = 0

def DalekDebugSetOutputDevice(_dalekDebugOutputDevice):
  global DalekDebugOutputDevice
  DalekDebugOutputDevice = _dalekDebugOutputDevice

def DalekDebugOn():
  global dalekDebugOn
  dalekDebugOn = True

def DalekDebugOff():
  global dalekDebugOn
  dalekDebugOn = False

def DalekPrint(text):
 
  if dalekDebugOn:
    if DalekDebugOutputDevice == 0:
      print(text)
    elif DalekDebugOutputDevice == 1:
      # put new device here
      pass

# on()
# off()
# on()

  # print("hello:{}".format(DalekDebugOn))


if __name__ == "__main__":
    print("\n\nDalekDebug.py cannot be run directly. It is intended to be imported\n\n")
else:
    print("Importing DalekDebug.py")