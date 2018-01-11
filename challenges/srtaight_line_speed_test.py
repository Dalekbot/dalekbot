def StraightLine():

    global speed               # Allow access to 'speed' constant
    global rightspeed          # Allow access to 'rightspeed' constant
    global leftspeed           # Allow access to 'leftspeed' constant
    global maxspeed            # Allow access to 'maxspeed' constant
    global minspeed            # Allow access to 'minspeed' constant
    global innerturnspeed      # Speed for Inner Wheels in a turn
    global outerturnspeed      # Speed for Outer Wheels in a turn
    global wii                 # Allow access to 'Wii' constants
    global soundvolume         # Allow access to sound volume
    global TrigPinLeft         # Allow Access to Trigger pin for Left Sensor
    global EchoPinLeft         # Allow Access to Echo pin for Left Sensor
    global TrigPinCenter       # Allow Access to Trigger pin for Right Sensor
    global EchoPinCenter       # Allow Access to Echo pin for Center Sensor
    global TrigPinRight        # Allow Access to Trigger pin for Right Sensor
    global EchoPinRight        # Set the Echo pin for Right Sensor
    
    leftdistance = 0           # Prime Left distance variable
    centerdistance = 0         # Prime Center distance variable
    rightdistance = 0          # Prime Right distance variable
    
    
        
    
    DalekPrint("Press 'A' to start Straight Line run","A")
    DalekPrint('Press "Hm" to return to main menu\n')
    time.sleep(.25)

    while True:
    
        buttons = wii.state['buttons']          # Get WiiMote Button Pressed

        if (buttons & cwiid.BTN_A):
            DalekPrint("Start Straight Line run","SLR")
            time.sleep(.25)
            
            while True:
            
                DalekV2Drive.forward(maxspeed)
            
                buttons = wii.state['buttons']          # Get WiiMote Button Pressed
                # Choose which task to do
                if (buttons & cwiid.BTN_HOME):
                    DalekV2Drive.stop()
                    DalekPrint("Press 'A' to start Streight Line run", "A")
                    DalekPrint("Press 'Hm' to return to main menu\n")
                    time.sleep(.25)
                    break
                # End if
                
                leftdistance = getdistance(leftdistance, TrigPinLeft, EchoPinLeft)
                centerdistance = getdistance(centerdistance, TrigPinCenter, EchoPinCenter)
                rightdistance = getdistance(rightdistance, TrigPinRight, EchoPinRight)
                
                scrollphat.write_string(str(leftdistance))
                print 'Left Distance :', leftdistance, 'Center Distance :', centerdistance, 'Right Distance :', rightdistance
                
                if centerdistance <= 2:
                    DalekV2Drive.stop()
                    print '\nCenter Distance :', centerdistance, 'Run Finished\n\n'
                    print'\nPress "A" to start Streight Line run'
                    print'Press "Hm" to return to main menu\n'
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string('"A"')
                    time.sleep(.25)
                    break
                # End if
                 
                if leftdistance <= 5:
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string('TrR')
                    DalekV2Drive.turnForwardRight(outerturnspeed, innerturnspeed)
                    time.sleep(.1)
                    DalekV2Drive.forward(maxspeed)
                # End if
                    
                if rightdistance <= 5:
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string('TrL')
                    DalekV2Drive.turnForwardLeft(innerturnspeed, outerturnspeed)
                    time.sleep(.1)
                    DalekV2Drive.forward(maxspeed)
                # End if

            # End While
                
        elif (buttons & cwiid.BTN_HOME):
            DalekV2Drive.stop()
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Hm")
            print "\n\nReturning to Main Menu\n\n"
            time.sleep(1)
            print "Main Menu"               # Show we are on main menu
            print '\nUp    - ObstacleCourse'
            print 'Down  - StreightLine'
            print 'Left  - MinimaMaze'
            print 'Right - Chase the Rainbow'
            print '1     - Line Follow'
#            print '2     - xxxxxx'
            print 'Home  - Exit\n'
            print "Ready"
            break
        # End if
    