def LineFollow(showcam):

    global speed               # Allow access to 'speed' constant
    global rightspeed          # Allow access to 'rightspeed' constant
    global leftspeed           # Allow access to 'leftspeed' constant
    global maxspeed            # Allow access to 'maxspeed' constant
    global minspeed            # Allow access to 'minspeed' constant
    global innerturnspeed      # Speed for Inner Wheels in a turn
    global outerturnspeed      # Speed for Outer Wheels in a turn
 
    global hRes                # Allow Access to Cam Horizontal Resolution
    global vRes                # Allow Access to Cam Vertical Resolution
    global video_capture       # Allow Access to WebCam Object
    global soundvolume         # Allow access to sound volume
    
    cx = 300                   # Go Streight
    turnspeed = 95
    speed = 30
    
    print'\nPress "A" to start Line following'
    print'Press "Hm" to return to main menu\n'
        
    scrollphat.clear()         # Shutdown Scroll pHat
    scrollphat.write_string('"A"')
    time.sleep(.25)

    while True:
    
        buttons = wii.state['buttons']          # Get WiiMote Button Pressed

        if (buttons & cwiid.BTN_A):
            print 'Start Line Following'
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('LiF')
            time.sleep(.25)
            cx = 300                   # Go Streight
            
            while True:
            
                buttons = wii.state['buttons']          # Get WiiMote Button Pressed
                # Choose which task to do
                if (buttons & cwiid.BTN_HOME):
                    DalekV2Drive.stop()
                    print'\nPress "A" to start Line following'
                    print'Press "Hm" to return to main menu\n'
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string('"A"')
                    time.sleep(.25)
                    break
            
                # Capture from camera
                ret, frame = video_capture.read()
     
                # Crop, select part of image to work with
                crop_img = frame[380:480, 0:640]

                # Make the image greyscale
                gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

                # uncomment next line to view greyscale image
                #cv2.imshow('Gray',gray) 
 
                # Apply a Gaussian blur
                blur = cv2.GaussianBlur(gray,(5,5),0)

                # uncomment next line to view Blurred image
                #cv2.imshow('Blur',blur)
 
                # Apply Color thresholding
                ret,thresh = cv2.threshold(blur,100,255,cv2.THRESH_BINARY_INV)

                # uncomment next line to view Threshholded image    
                #cv2.imshow('Thresh',thresh)
 
                # Find the contours in the cropped image part
                img, contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

                # ---------------- Find the biggest contour = line -----------------
    
                if len(contours) > 0:
                    c = max(contours, key=cv2.contourArea)
                    M = cv2.moments(c)
 
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
 
                    cv2.line(crop_img,(cx,0),(cx,720),(255,255,0),2)
                    cv2.line(crop_img,(0,cy),(1280,cy),(0,255,0),2)
                    cv2.drawContours(crop_img, contours, -1, (0,255,255), 2)

                    # ---- Draw centre boundry lines (Steer straight)
                    cv2.line(crop_img,(270,0),(270,480),(0,0,255),2)
                    cv2.line(crop_img,(370,0),(370,480),(0,0,255),2)

                # --------- Steer Right Routine ----------
                if cx >= 370:
                    RSteer = cx - 370
                    SteerRight = remap(RSteer, 0, 45, 1, 270)
                    print "Turn Right: ", SteerRight, cx
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string("TrR")
                    DalekV2Drive.spinRight(turnspeed)

                # --------- On Track Routine ----------
                if cx < 370 and cx > 270:
                    print "On Track", cx
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string("Fw")
                    DalekV2Drive.forward(speed)

                # --------- Steer Left Routine ----------
                if cx <= 270:
                    LSteer = 270 - cx
                    SteerLeft = remap(LSteer, 0, 45, 1, 270)
                    print "Turn Left: ", SteerLeft, cx
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string("TrL")
                    DalekV2Drive.spinLeft(turnspeed)
 
                # ------ Show the resulting cropped image
                if showcam == True:
                    cv2.imshow('frame',crop_img)
                # ------ Exit if Q pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                                
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