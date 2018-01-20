import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )


from  dalek import spi 
from dalek import debug 
import time
      
spi.init()  

data =spi.SensorData()

data.start()

print("started")

while True:
  for i in range(100000):
    print("\n      {}" .format(i))
    time.sleep(2)
    