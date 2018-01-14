#!/usr/bin/env python

import time
import DalekV2DriveV2

import DalekSpi

import RPi.GPIO as GPIO  # Import GPIO divers
GPIO.setwarnings(False)

DalekV2DriveV2.init()
DalekSpi.init()


# this gets the spi reading and gets rid of bad readings and
# readings that are out of range due to the motors and acceleration


def getStartingMag():
     # used for all timings in this function.
    timerTime = 0.4
    magOffset = 3000
    print("\n-getStartingMag()")
    DalekV2DriveV2.stop()
    time.sleep(timerTime)
    currentMag = -1
    while not (0 <= currentMag <= 360): # ensure we get a valid reading must be between 0 and 360
      currentMag = DalekSpi.getMag()
     
    print("--currentMag:{}\n-------------\n".format(currentMag))
    currentMag +=  magOffset # add the offset value
    return currentMag 


def getMag(clockwise=True ,currentHeading=None):
    # used for all timings in this function.
    timerTime = 0.4

    # The value we add to all readings to
    # get over the 360 to 0 rollover and all the
    # calculations that would be needed.
    # use a high number so it stays above Zero
    magOffset = 3000
    currentMag = -1 # set a value that we can not get.
    print("\n1---getMag({},{})".format(clockwise, currentHeading - magOffset))
    if currentHeading == None: 
      return getStartingMag()
    else:
      previousMagReading = currentHeading - magOffset # subtract off the offset to get previous reading.
      print("\n2---getMag({},{})".format(direction, previousMagReading - magOffset))
       
       
      if previousMagReading > 360:
        floorDivisionOfPreviousMagReading = previousMagReading // 360 # should be 1,2 or 3
        previousMagReading = previousMagReading  % 360                # between 0 and 360
        magOffset += (floorDivisionOfPreviousMagReading * 360) # add the back for using later
        print("\n   getMag() previousMagReading > 360  previousMagReading:{}  magOffset:{} ".format( previousMagReading, magOffset))
        
      
      #####################
      ## TODO this should now wrk for clockwise
      # now do anticlockwise
     
      # now we can get a new value.
      DalekSpi.stop()
      time.sleep(timerTime) # settle the bot for better reading

      if clockwise: # Clockwise 
        currentMag = DalekSpi.getMag()
        if 0 <=  currentMag <= 360: # is between 0 and 360
          #  is between previous reading and an upper limit this prevents errors if 
          #  the mag is affected buy other factors.
          if previousMagReading <= currentMag  <= (previousMagReading +30):
            currentMag += magOffset
            print("---Clockwise {}".format(currentMag))
          # you have rolled over the 360 mark
          #      val: 355         <=    (5 + 360){365}   <=  ( 355 + 30{385}) = True
          elif previousMagReading <= (currentMag + 360 ) <= (previousMagReading +30):
            currentMag += 360 + magOffset
            print("---Clockwise Rollover{}".format(currentMag))
          else:
            print("---error in mag reading out of range currentMag:{}".format(currentMag))
        
        else:
          print("--error in mag reading > 360 value:{}".format(currentMag))
        return currentMag  



      else: #  anti Clockwise
        pass



    magMax = currentMag + currentMagPlay
    minMag = currentMag - currentMagPlay

    # while the mag reading is not between the range we set
    # keep trying for a more accurate reading.
    while not (minMag < currentMag <= magMax):
        DalekSpi.stop()
        time.sleep(timerTime)
        currentMag = DalekSpi.getMag() + magOffset
        

    return currentMag


def DalekTurn(degreesToTurn):
    magOffset = 3000
    # used for all timings in this function.
    timerTime = 0.4
    fastModeSpeed = 60
    normalModeSpeed = 25

    print("\n---------")
    print("DalekTurn({})".format(degreesToTurn))
    

    startHeading = getStartingMag()
    currentHeading = startHeading
    endHeading = startHeading + degreesToTurn
    print("\n################ \nStartHeading:{} CurrentHeading:{} EndHeading:{}".format(
        (startHeading - magOffset), (currentHeading- magOffset), (endHeading - magOffset)))
   
    # used to hold any pass of the 360/0 point
    pass360Point=0
    


    # turn counter clockwise
    if  degreesToTurn < 0:
      print("turn counter clockwise")



      counter = 0
      while endHeading <= currentHeading:

        if (  currentHeading - endHeading >= 60):
          print("#### FAST MODE ##### ")
          ## subtract off the endHeading so is dose not over shoot.
          pass360Point = turnAntiClockwise(currentHeading, endHeading + 30, timerTime, pass360Point, fastModeSpeed)
          time.sleep(timerTime)
          currentHeading = getMag(True,currentHeading)

        pass360Point = turnAntiClockwise(currentHeading, endHeading, timerTime, pass360Point, normalModeSpeed)
        time.sleep(timerTime)
        currentHeading = getMag(True,currentHeading)
        print(" currentHeading Heading:{} should be:{}    pass360Point:{}"
                       .format((currentHeading - magOffset),( (endHeading- magOffset) - pass360Point),pass360Point))
        
        if counter == 5:
          break  




    # turn  clockwise
    elif degreesToTurn > 0:   
      
      counter = 0
      while   endHeading >= currentHeading:

        if (endHeading - currentHeading >= 60):
          print("#### FAST MODE ##### ")
          ## subtract off the endHeading so is dose not over shoot.
          pass360Point = turnClockwise(currentHeading, endHeading - 30, timerTime, pass360Point, fastModeSpeed)
          time.sleep(timerTime)
          currentHeading = getMag(True,currentHeading)
          
        
        pass360Point = turnClockwise(currentHeading, endHeading, timerTime, pass360Point, normalModeSpeed)
        
        time.sleep(timerTime)
        currentHeading = getMag(True,currentHeading)


        print(" currentHeading Heading:{} should be:{}    pass360Point:{}".format((currentHeading - magOffset),( (endHeading- magOffset) - pass360Point),pass360Point))
        
        
        if counter == 5:
          break
        

    # you entered 0 so exit
    else:
      pass 
    
    DalekV2DriveV2.stop()
    time.sleep(timerTime)
    # mag = getMag() - magOffset
    print("-- End Heading:{} should be:{}".format((getMag() - magOffset),( (endHeading- magOffset) - pass360Point)))




# this is a private function used in the DalekTurn function
def turnClockwise(currentHeading, endHeading, timerTime, pass360Point,_speed):
  magOffset = 3000
  print("---- turnClockwise\n speed{}".format(_speed))

  minval = currentHeading
  while currentHeading <= endHeading:
    time.sleep(timerTime) # pause for sensor to settel
    checkforPass360 =getMag(True,currentHeading)
    DalekV2DriveV2.spinRight(_speed)
    
    print("  checkforPass360: {}".format(checkforPass360 - magOffset))
    # take a little off it to account for reading error.
    # 3 < (350 -100)  or 3 < 250 is true
    # 350 < 250 is false, not passed zero point
    # you wont move more than 100 dec in 0.3 seconds
    if checkforPass360 < (currentHeading -100):
      checkforPass360 = checkforPass360 + 360 # you have passed 360
      pass360Point = pass360Point + 360       # add to the return value.
    if currentHeading < checkforPass360:
     currentHeading = checkforPass360          # this is now your new value


    print("  currentHeading:  {}".format(currentHeading - magOffset))
  DalekV2DriveV2.stop()
  print("---------------------exit turnClockwise\n" )  
  return pass360Point



# this is a private function used in the DalekTurn function
def turnAntiClockwise(currentHeading, endHeading, timerTime, pass360Point,speed):
  magOffset = 3000
  print("--------------------- turnAntiClockwise\n speed{}".format(speed))
  while currentHeading >= endHeading:
    time.sleep(timerTime)
    checkforPass360 =getMag()
    DalekV2DriveV2.spinLeft(speed)

    print("  checkforPass360: {}".format(checkforPass360 - magOffset))
    # take a little off it to account for reading error.
    if checkforPass360 > (currentHeading + 100):
      checkforPass360 = checkforPass360 - 360
      pass360Point = -360
    currentHeading = checkforPass360

    print("  currentHeading:  {}".format(currentHeading - magOffset))
  DalekV2DriveV2.stop()
  print("---------------------exit turnAntiClockwise\n")
  return pass360Point    

 

def test():  
    magOffset = 3000
    
    # DalekTurn(-90)
    # print("#########################\n")
    # time.sleep(stop)
    DalekTurn(90)
    #print("#########################\n")
    print("#########################\n")
    # time.sleep(stop)
    # DalekTurn(-45)
    # print("#########################\n")
    # time.sleep(stop)
    # DalekTurn(45)

    # DalekTurn(-25)
    # DalekTurn(65)
    startval = mag-magOffset
    endval = getMag(0, startval) - magOffset
    print("\n\n########################\nstart:{} End{}".format(startval,endval))


test()
