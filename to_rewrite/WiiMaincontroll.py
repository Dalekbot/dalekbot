def maincontrol(showcam):                  # Main Control Loop

    global wii                      # Allow access to 'Wii' constants
    global soundvolume              # Allow access to sound volume

    scrollphat.clear()              # Clear Scroll pHat
    scrollphat.write_string("Mn")   # Show we are on main menu
    print "Main Menu"               # Show we are on main menu

    print '\nUp    - ObstacleCourse'
    print 'Down  - StraightLine'
    print 'Left  - MinimaMaze'
    print 'Right - Chase the Rainbow'
    print '1     - Line Follow'
#    print '2     - xxxxxx'
    print 'Home  - Exit\n'
    
    wii.rpt_mode = cwiid.RPT_BTN

    print "Ready"
    
    while True:
    
        scrollphat.clear()              # Clear Scroll pHat
        scrollphat.write_string("Mn")   # Show we are on main menu

        buttons = wii.state['buttons']          # Get WiiMote Button Pressed
        # Choose which task to do
     
        # If Plus and Minus buttons pressed
        # together then rumble and quit.
        if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):  
            break  
 
        if (buttons & cwiid.BTN_UP):
            print 'ObstacleCourse'
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string("OC")
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(["mplayer",volumesetting, "Sound/Rant.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ObstacleCourse()
        elif (buttons & cwiid.BTN_DOWN):
            print 'StreightLine'
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string("StL")
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(["mplayer",volumesetting, "Sound/Stay.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)
            StreightLine()
        elif (buttons & cwiid.BTN_LEFT):
            print 'MinimalMaze'
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string("MM")
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(["mplayer",volumesetting, "Sound/IntruderLocated.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)
            #MinimalMaze()
        elif (buttons & cwiid.BTN_RIGHT):
            print 'Chase the Rainbow'
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string("CtR")
            time.sleep(1)
            Rainbow(showcam)
        elif (buttons & cwiid.BTN_1):
            print 'Line Follow'
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string("LiF")
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(["mplayer",volumesetting, "Sound/IntruderLocated.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            LineFollow(showcam)
#        elif (buttons & cwiid.BTN_2):
#            print 'xxxxxx'
#            scrollphat.clear()         # Clear Scroll pHat
#            scrollphat.write_string("LiF")
#            LineFollowPiCam(showcam)
        elif (buttons & cwiid.BTN_PLUS):
            print '+'
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string("+")
            volumesetting = '"--volume=' + str(soundvolume) +'"'
            subprocess.Popen(["mplayer",volumesetting, "Sound/exterminate.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif (buttons & cwiid.BTN_MINUS):
            print '-'
            scrollphat.clear()         # Clear Scroll pHat
            scrollphat.write_string("-")
        elif (buttons & cwiid.BTN_HOME): #or (buttons & cwiid.BTN_A):
            break

        DalekV2Drive.stop()

# End of Main Control Procedure 