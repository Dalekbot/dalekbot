import time
import DalekV2DriveV2

import DalekSpi 
import RPi.GPIO as GPIO  # Import GPIO divers
GPIO.setwarnings(False)


DalekV2DriveV2.init()
speed = 50

DalekSpi.init()

def DalekTurn(degreesToTurn):
    DalekTurn1(degreesToTurn)
    mag =DalekSpi.getMag()
    if mag < 


def DalekTurn1(degreesToTurn):

    print("\n---------")
    print("DalekTurn({})".format(degreesToTurn))
    print("speed{}".format(speed))
    startHeading = DalekSpi.getMag()
    currentHeading = startHeading
    endHeading = 0
    rotationsFull = 0
    rotationDegrees = 0
    direction = 0

    # normalise the data a
    if degreesToTurn < 0:
        direction = 1  # 0 clockwise , 1 anticlockwise
        degreesToTurn = -degreesToTurn

     # Calculate if more than one rotation
    if degreesToTurn > 360:
        rotationsFull = int(degreesToTurn / 360)
        rotationDegrees = int(degreesToTurn % 360)
    else:
        rotationDegrees = degreesToTurn

    print("  Rotations:{} then Deg:{}  "    .format(
        rotationsFull, rotationDegrees))

    # Clockwise rotation
    if direction == 0:

        # check if it goes past 360
        if (startHeading + rotationDegrees) > 360:
            endHeading = startHeading + rotationDegrees - 360
            rotationsFull += 1
            print(" Rolls over 360")
            print("A: currrent:{}  :{} Rotation then Deg:{} endheading:{}" .format(
                currentHeading, rotationsFull, rotationDegrees, endHeading))

        else:
            endHeading = startHeading + rotationDegrees
            print("B:  currrent:{}  :{}Full Rotations, then Deg:{} --- endheading:{}" .format(
                currentHeading, rotationsFull, rotationDegrees, endHeading))
            print("  clockwise rotation")
        lastHeading = currentHeading

        # while (currentHeading -5 ) <=
        #  endHeading <= (currentHeading +5): # between 5 either side
        DalekV2DriveV2.spinRight(speed)
        
        
        
        # if there is a rotation passed 360 then look for it
        while rotationsFull > 0:
            DalekV2DriveV2.spinRight(speed)
            # mag = DalekSpi.getMag()
            print("going passed 306")
            #time.sleep(.1)
            
            # not passed 360 yet
            while currentHeading > endHeading:
                DalekV2DriveV2.spinRight(speed)
                currentHeading = denoiseGetMag(currentHeading)
                print("  currentHeading:{}".format(currentHeading))
                time.sleep(.1)

            # you are now passed 360 
            if  (currentHeading  <= endHeading):
                rotationsFull = 0
                print("  Passed 360")

        while (endHeading >= currentHeading)  :  # between 5 either side
            DalekV2DriveV2.spinRight(speed)
            print("  speed:{}".format(speed))
            time.sleep(.1)
            DalekV2DriveV2.stop()
           
            currentHeading = denoiseGetMag(currentHeading)
            print("  currrent:{}  :{} Rotation then Deg:{} endheading:{}" .format(
                currentHeading, rotationsFull, rotationDegrees, endHeading))
            lastHeading = currentHeading

            # if currentHeading <= (lastHeading):  # gone past the 360 point
                # rotationsFull -= 1
                

        print("done currentHeading:{}".format(currentHeading))
        DalekV2DriveV2.stop()

    # anticlockwise rotation
    else:
        print("  anticlockwise rotation")


def denoiseGetMag(_currentreading):
    
    # if the new reading is too big there is an error
    # so discard it
    amount = 30
    timer = 0.1
    version_a =0.8
    maxMag = _currentreading + 30
    minMag = _currentreading - 30
    clockwisePass360 = False
    anticlockwisePass360 = False

    if (maxMag >= 360):
        maxMag = maxMag - 360
        clockwisePass360 = True
    if (minMag < 0):
        minMag = 360 + minMag
        anticlockwisePass360 = True
    
    currentReading = DalekSpi.getMag()
    while currentReading > 360:
       currentReading = DalekSpi.getMag()    
    
    if clockwisePass360:
        while  (minMag <= currentReading <= 360) ==True or ( 0 <= currentReading <= maxMag) ==True:
            currentReading = DalekSpi.getMag()
            time.sleep(timer)
            d1 =( minMag <= currentReading <= 360)
            d2 =  ( 0 <= currentReading <= maxMag)
            print("dn A v{}: currentReading:{} mix:{} max{} {}{}" .format(version_a,currentReading,minMag, maxMag,d1,d2))
    
    
    
    
    elif anticlockwisePass360:      
        while  (minMag <= currentReading <= 360) or ( 0 <= currentReading <= maxMag) ==False:
            currentReading = DalekSpi.getMag()
            time.sleep(timer)
            d1 = (minMag <= currentReading <= 360)
            d2 =  ( 0 <= currentReading <= maxMag)
            print("dn B v{}: currentReading:{} mix:{} max{} {}{}" .format(version_a,currentReading,minMag, maxMag,d1,d2))
    
    
    
    else:
        while not (minMag <= currentReading <= maxMag):
            currentReading = DalekSpi.getMag()
            time.sleep(timer)
            d1 = (minMag <= currentReading <= maxMag)
            print("dn c v{}: currentReading:{} mix:{} max{} {}{}" .format(version_a,currentReading,minMag, maxMag,d1))

 


    
    print("currentReading:{} mix:{} max{}" .format(currentReading,minMag, maxMag))
    return currentReading
   
    
       

         
    

# print("\n\n-----------------------------------------------------------")
# print("start deg:{}".format(DalekSpi.getMag()))
# print( DalekSpi.getMag())
# print( DalekSpi.getMag())
# print( DalekSpi.getMag())
# print( DalekSpi.getMag())
# print( DalekSpi.getMag())
# DalekTurn(-395)
# DalekTurn(45)


# while True:
#   print( DalekSpi.getMag())
#   time.sleep(.5)
# DalekV2DriveV2.cleanup()
 #  __main__ Code
#======================================================================	   
    
if __name__ == "__main__":
    print("\n\nThis file cannot be run directly. It is intended to be imported\n\n")
else:
    print("\n\nImporting autoDrive2.py")
    
# End of __main__ Code
#======================================================================