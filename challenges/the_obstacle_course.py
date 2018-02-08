def ObstacleCourse():

    global speed               # Allow access to 'speed' constant
    global rightspeed          # Allow access to 'rightspeed' constant
    global leftspeed           # Allow access to 'leftspeed' constant
    global maxspeed            # Allow access to 'maxspeed' constant
    global minspeed            # Allow access to 'minspeed' constant
    global innerturnspeed      # Speed for Inner Wheels in a turn
    global outerturnspeed      # Speed for Outer Wheels in a turn
    global wii                 # Allow access to 'Wii' constants
    global soundvolume         # Allow access to sound volume

    wii.rpt_mode = cwiid.RPT_BTN

    time.sleep(2)

    boost = 0                                   # Turn boost off

    while True:
        buttons = wii.state['buttons']          # Get WiiMote Button Pressed
        # Choose which task to do

        # If Plus and Minus buttons pressed
        # together then rumble and quit.
        if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
            break

        print speed
        scrollphat.clear()         # Shutdown Scroll pHat
        scrollphat.write_string(str(speed))

        if boost == 0 and (buttons & cwiid.BTN_B):
            print 'Boost', maxspeed
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Max")
            savespeed = speed
            speed = maxspeed
            boost = 1
            time.sleep(.25)
        elif boost == 1 and (buttons & cwiid.BTN_B):
            speed = savespeed
            boost = 0
            print 'Normal', speed
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Nor")
            time.sleep(.25)

        if (buttons & cwiid.BTN_UP):
            print 'Forward', speed
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Fw")
            DalekV2Drive.forward(speed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_DOWN):
            print 'Backward', speed
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Bw")
            DalekV2Drive.backward(speed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_LEFT):
            print 'Spin Left', speed
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("SL")
            DalekV2Drive.spinLeft(maxspeed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_RIGHT):
            print 'Spin Right', speed
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("SR")
            DalekV2Drive.spinRight(maxspeed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_1):
            print 'Turn Right'
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("TrR")
            DalekV2Drive.turnForwardRight(outerturnspeed, innerturnspeed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_2):
            print 'Turn Left'
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("TrL")
            DalekV2Drive.turnForwardLeft(innerturnspeed, outerturnspeed)
            time.sleep(.25)
        elif (buttons & cwiid.BTN_PLUS):
            print 'Speed Up 1'
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("+1")
            if speed < 100:
                speed = speed + 1
                time.sleep(0.5)
        elif (buttons & cwiid.BTN_MINUS):
            print 'Speed Down 1'
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("-1")
            if speed > 0:
                speed = speed - 1
                time.sleep(0.5)
        elif (buttons & cwiid.BTN_A):
            print 'Stop'
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string("Stp")
            DalekV2Drive.stop()
            time.sleep(.25)
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
