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
    timerTime = 0.0
    magOffset = 3000
    # print("\n--getStartingMag()")
    DalekV2DriveV2.stop()
    time.sleep(timerTime)
    currentMag = -1
    while not (0 <= currentMag <= 360): # ensure we get a valid reading must be between 0 and 360
      currentMag = DalekSpi.getMag()
     
    currentMag +=  magOffset # add the offset value
    print("---getStartingMag:{}".format(currentMag - magOffset))
    return currentMag 


def getMag(stopingTime,clockwise=True ,currentHeading=None):
    # used for all timings in this function.
    timerTime = stopingTime

    # The value we add to all readings to
    # get over the 360 to 0 rollover and all the
    # calculations that would be needed.
    # use a high number so it stays above Zero
    magOffset = 3000
    currentMag = -1 # set a value that we can not get.
    # print("\n1---getMag({},{})".format(clockwise, currentHeading ))

    if currentHeading == None: 
      return getStartingMag()
    else:
      previousMagReading = currentHeading - magOffset # subtract off the offset to get previous reading.
      # print("2---getMag({},{}\n)".format(clockwise, previousMagReading ))

      if previousMagReading > 360:
        floorDivisionOfPreviousMagReading = previousMagReading // 360 # should be 1,2 or 3
        previousMagReading = previousMagReading  % 360                # between 0 and 360
        magOffset += (floorDivisionOfPreviousMagReading * 360) # add the back for using later
        # print("\n----getMag() previousMagReading > 360  previousMagReading:{}  magOffset:{})  ".format( previousMagReading, magOffset))
        
      
      # now we can get a new value.
      DalekV2DriveV2.stop()
      time.sleep(timerTime) # settle the bot for better reading
##################################################################################
      
      magErrorOfset = 60
      if clockwise: # Clockwise

        currentMag = DalekSpi.getMag()
        if 0 <=  currentMag <= 360: # is between 0 and 360
          #  is between previous reading and an upper limit this prevents errors if 
          #  the mag is affected buy other factors.
          if previousMagReading <= currentMag  <= (previousMagReading +40):
            currentMag += magOffset
            # print("-------Clockwise {}".format(currentMag))
          # you have rolled over the 360 mark
          #      val: 355         <=    (5 + 360){365}   <=  ( 355 + 30{385}) = True
          elif previousMagReading <= (currentMag + 360 ) <= (previousMagReading + magErrorOfset):
            currentMag += 360 + magOffset
            # print("-------Clockwise Rollover{}".format(currentMag))
          else:
            if currentMag  > (previousMagReading + magErrorOfset):
              print("------error  mag reading too high:{}".format(currentMag))
              DalekV2DriveV2.stop() # make sure we have stopped
              time.sleep(.5) # now wait again to settle
              tempcurrentMag = DalekSpi.getMag() # get another reading  this one we will go with.
              print("4                                  mag now {}".format(tempcurrentMag))
            
        
        else:
          print("-----error in mag reading > 360 value:{}".format(currentMag))
          currentMag = currentHeading 
        


      # elif clockwise == False:
      #    print("---asdafdsasdf---anti Clockwise:{}".format(currentMag))
      else: #  anti Clockwise
        currentMag = DalekSpi.getMag()
        # print("1------anti Clockwise:{}".format(currentMag))
        
        if 0 <=  currentMag <= 360: # is between 0 and 360
             #   120 -40{80}           <=  100      <=   120     
          if (previousMagReading - magErrorOfset) <= currentMag <= previousMagReading:
            currentMag += magOffset
            # print("2-------antiClockwise {}".format(currentMag))
           
          elif previousMagReading - magErrorOfset <= (currentMag - 360) <= previousMagReading:
            currentMag -= 360 - magOffset
            print("3-------antiClockwise Rollover{}".format(currentMag))
          else:
            if (previousMagReading - magErrorOfset) <= currentMag:
              print("4------error  mag reading too low:{}".format(currentMag))
              DalekV2DriveV2.stop() # make sure we have stopped
              time.sleep(.5) # now wait again to settle
              tempcurrentMag = DalekSpi.getMag() # get another reading  this one we will go with.
              print("4                                  mag now {}".format(tempcurrentMag))
            
        else:
          print("-----error in mag reading > 360 value:{}".format(currentMag))
          currentMag = currentHeading 
            


    return currentMag    





def DalekTurn(degreesToTurn):
    magOffset = 3000
    # used for all timings in this function.
    # timerTime = 0.1
    fastModeSpeed = 50
    normalModeSpeed = 35
    slowModeSpeed = 25
    runTime = 1

    print("\n#################")
    print("DalekTurn({})".format(degreesToTurn))
    

    startHeading = getStartingMag()
    currentHeading = startHeading
    endHeading = startHeading + degreesToTurn
    print("#################\nStartHeading:{} CurrentHeading:{} EndHeading:{}".format(
        (startHeading - magOffset), (currentHeading- magOffset), (endHeading - magOffset)))
   
    # used to hold any pass of the 360/0 point
    pass360Point=0
    

   
    # turn counter clockwise
    if  degreesToTurn < 0:
      print("turn counter clockwise")



      counter = 0
      while endHeading < currentHeading:
        
        if ( currentHeading - endHeading >= 40):
          print("#### FAST MODE ##### ")
          ## subtract off the endHeading so is dose not over shoot.
          currentHeading = turnAntiClockwise(currentHeading, endHeading + 30, fastModeSpeed )
         
        if (currentHeading - endHeading  >= 20):
          print("#### NORMAL MODE ##### ")
          ## subtract off the endHeading so is dose not over shoot.
          currentHeading = turnAntiClockwise(currentHeading, endHeading + 20, normalModeSpeed)
          
        print("#### SLOW MODE ##### ")
        currentHeading = turnAntiClockwise(currentHeading, endHeading, slowModeSpeed)
      
      DalekV2DriveV2.stop()
      startval= currentHeading - magOffset
      endval = (endHeading % 360)- magOffset
      print(" End Heading:{} should be:{}".format(startval,endHeading- magOffset ))




    # turn  clockwise
    elif degreesToTurn > 0:   
      
     
      while   endHeading > currentHeading:

        if (endHeading - currentHeading >= 40):
          print("#### FAST MODE ##### ")
          ## subtract off the endHeading so is dose not over shoot.
          currentHeading = turnClockwise(currentHeading, endHeading - 30, fastModeSpeed )
          # currentHeading = getMag(True,currentHeading)
        if (endHeading - currentHeading >= 20):
          print("#### NORMAL MODE ##### ")
          ## subtract off the endHeading so is dose not over shoot.
          currentHeading = turnClockwise(currentHeading, endHeading - 20, normalModeSpeed )
          # currentHeading = getMag(True,currentHeading)  
        print("#### SLOW MODE ##### ")
        currentHeading = turnClockwise(currentHeading, endHeading, slowModeSpeed)
       
      DalekV2DriveV2.stop()
      startval= currentHeading - magOffset
      endval = (endHeading % 360)- magOffset
      print(" End Heading:{} should be:{}".format(startval,endHeading - magOffset))
          
        
        

    # you entered 0 so exit
    else:
      DalekV2DriveV2.stop()
    
    DalekV2DriveV2.stop()
   
def magTurn(currentHeading, endHeading, speed,clockwise=True):
  print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
  print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
  debugDirection = "turnAntiClockwise"
  if clockwise:
    debugDirection = "turnClockwise"
    
  stopingTime = 0.3
  if speed > 45:
    stopingTime = 0.1
  elif speed >= 26:
    stopingTime = 0.3
    
  print("-START magTurn_{}({},{},{})".format(debugDirection,currentHeading,endHeading,speed))
  while endHeading > currentHeading:
    print("---turnClockwise() currentHeading: {}".format(currentHeading - 3000))
    for  i in range(10 ,speed ):

      if clockwise: 
        DalekV2DriveV2.spinRight(speed)
        time.sleep(stopingTime)
      else:
        DalekV2DriveV2.spinLeft(speed)
        time.sleep(stopingTime)
    currentHeading =getMag(stopingTime,True,currentHeading, )
   
  print("-done.")
  return currentHeading
    

          


def turnClockwise(currentHeading, endHeading, speed):
  
  stopingTime = 0.3
  if speed > 45:
    stopingTime = 0.1
  elif speed >= 26:
    stopingTime = 0.3
    
  print("-START turnClockwise({},{},{})".format(currentHeading,endHeading,speed))
  while endHeading > currentHeading:
    print("---turnClockwise() currentHeading: {}".format(currentHeading - 3000))
    for  i in range(10 ,speed ):
      DalekV2DriveV2.spinRight(speed)
      time.sleep(0.015)
    currentHeading =getMag(stopingTime,True,currentHeading, )
   
  print("-done.")
  return currentHeading



def turnAntiClockwise(currentHeading, endHeading, speed):
  
  stopingTime = 0.3
  if speed > 45:
    stopingTime = 0.1
  elif speed >= 26:
    stopingTime = 0.4
    
  print("-START turnAntiClockwise({},{},{})".format(currentHeading,endHeading,speed))
  while endHeading < currentHeading:
    print("---turnAntiClockwise() currentHeading: {}".format(currentHeading - 3000))
    for  i in range(10 ,speed ):
      DalekV2DriveV2.spinLeft(speed)
      time.sleep(0.015)
    currentHeading =getMag(stopingTime,False,currentHeading )
   
  print("-done.")
  return currentHeading







def test():  
    magOffset = 3000
    
    # DalekTurn(-90)
    # print("#########################\n")
    # time.sleep(stop)
    # time.sleep(.5)

    for i in range(0 , 8):
      # DalekV2DriveV2.forward(30)
      # time.sleep( 1)
      DalekTurn(-45)
      DalekTurn(45)
    # for i in range(0 , 8):
      # DalekV2DriveV2.backward(30)
      # time.sleep( 1)
    # DalekV2DriveV2.forward(30)
    # DalekTurn(90)
    # DalekV2DriveV2.forward(30)
    # DalekTurn(90) 
    # DalekV2DriveV2.forward(30)
    # DalekTurn(90)
    
    # DalekTurn(360)
    # DalekV2DriveV2.backward(30)
    # DalekTurn(-180)
    # DalekV2DriveV2.stop()
    #print("#########################\n")
    print("#########################\n")
    # time.sleep(stop)
    # DalekTurn(-45)
    # print("#########################\n")
    # time.sleep(stop)
    # DalekTurn(45)

    # DalekTurn(-25)
    # DalekTurn(65)
    # startval = mag-magOffset
    # endval = getStartingMag() - magOffset
    # print("\n\n########################\nstart:{} End{}".format(startval,endval))


test()
