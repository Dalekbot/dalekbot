def Rainbow(showcam):

    global speed               # Allow access to 'speed' constant
    global rightspeed          # Allow access to 'rightspeed' constant
    global leftspeed           # Allow access to 'leftspeed' constant
    global maxspeed            # Allow access to 'maxspeed' constant
    global minspeed            # Allow access to 'minspeed' constant
    global innerturnspeed      # Speed for Inner Wheels in a turn
    global outerturnspeed      # Speed for Outer Wheels in a turn
    global wii                 # Allow access to 'Wii' constants
    global hRes                # Allow Access to Cam Horizontal Resolution
    global vRes                # Allow Access to Cam Vertical Resolution
    global video_capture       # Allow Access to WebCam Object
    global soundvolume         # Allow access to sound volume

    turnspeed = 95

    print "Checkpoint: Set up WebCam\n"
    # initialize the camera and grab a reference to the raw camera capture

    hRes = 320
    vRes = 240

    print "default resolution = " + str(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, hRes)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, vRes)

    print "updated resolution = " + str(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

#    if video_capture.isOpened() == False:                           # check if VideoCapture object was associated to webcam successfully
#        print "error: video_capture not accessed successfully\n\n"  # if not, print error message to std out
#        os.system("pause")                                          # pause until user presses a key so user can see error message
#        wait = input("PRESS ENTER TO CONTINUE.\n\n")
#        return                                                      # and exit function (which exits program)
#    # end if

    intXFrameCenter = int(
        float(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)) / 2.0)
    intYFrameCenter = int(
        float(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) / 2.0)

    # print intXFrameCenter, intYFrameCenter

    if intXFrameCenter == 0.0:
        scrollphat.clear()         # Shutdown Scroll pHat
        scrollphat.write_string('Err')
        time.sleep(2)
        return

    panServoPosition = intXFrameCenter

    print'\nPress "A" to Chase the Rainbow'
    print'Press "Hm" to return to main menu\n'

    scrollphat.clear()         # Shutdown Scroll pHat
    scrollphat.write_string('"A"')
    time.sleep(.25)

    # print "Checkpoint: Enter main Loop\n\n"

    while True:

        buttons = wii.state['buttons']          # Get WiiMote Button Pressed

        if (buttons & cwiid.BTN_A):
            print 'Start Chasing the Rainbow'
            scrollphat.clear()         # Shutdown Scroll pHat
            scrollphat.write_string('CtR')
            time.sleep(.25)

            while True:

                # Get WiiMote Button Pressed
                buttons = wii.state['buttons']

                if (buttons & cwiid.BTN_HOME):
                    DalekV2Drive.stop()
                    print'\nPress "A" to Chase the Rainbow 1 '
                    print'Press "Hm" to return to main menu\n'
                    scrollphat.clear()         # Shutdown Scroll pHat
                    scrollphat.write_string('"A"')
                    time.sleep(.25)
                    break

                # cv2.waitKey(1) != 32 and until the Esc key is pressed or webcam connection is lost
                while video_capture.isOpened():
                    blnFrameReadSuccessfully, imgOriginal = video_capture.read()            # read next frame

                    # Get WiiMote Button Pressed
                    buttons = wii.state['buttons']

                    if (buttons & cwiid.BTN_HOME):
                        DalekV2Drive.stop()
                        print'\nPress "A" to Chase the Rainbow 2'
                        print'Press "Hm" to return to main menu\n'
                        scrollphat.clear()         # Shutdown Scroll pHat
                        scrollphat.write_string('"A"')
                        time.sleep(.25)
                        break
                    # end if

                    if not blnFrameReadSuccessfully or imgOriginal is None:             # if frame was not read successfully
                        # print error message to std out
                        print "error: frame not read from webcam\n"
                        # os.system("pause")                                             # pause until user presses a key so user can see error message
                        # exit while loop (which exits program)
                        break
                    # end if

                    # print "Checkpoint: Picture Taken - Starting Analysis"

                    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

                    imgThreshLow = cv2.inRange(imgHSV, np.array(
                        [0, 135, 135]), np.array([19, 255, 255]))
                    imgThreshHigh = cv2.inRange(imgHSV, np.array(
                        [168, 135, 135]), np.array([179, 255, 255]))

                    imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

                    imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)

                    imgThresh = cv2.dilate(
                        imgThresh, np.ones((5, 5), np.uint8))
                    imgThresh = cv2.erode(imgThresh, np.ones((5, 5), np.uint8))

                    intRows, intColumns = imgThresh.shape

                    # print "Checkpoint : 2"

                    # fill variable circles with all circles in the processed image
                    circles = cv2.HoughCircles(
                        imgThresh, cv2.HOUGH_GRADIENT, 3, intRows / 4)

                    # this line is necessary to keep program from crashing on next line if no circles were found
                    if circles is not None:

                        sortedCircles = sorted(
                            circles[0], key=itemgetter(2), reverse=True)

                        largestCircle = sortedCircles[0]

                        # break out x, y, and radius
                        x, y, radius = largestCircle
                        # print ball position and radius
                        print "ball position x = " + str(x) + ", y = " + str(y) + ", radius = " + str(radius)

                        scrollphat.clear()
                        scrollphat.write_string("Red")
                        DalekV2Drive.forward(speed)

                        if x < intXFrameCenter and panServoPosition >= 2:
                            panServoPosition = panServoPosition - 2
                            print "Turn Left: ", panServoPosition
                            scrollphat.clear()         # Shutdown Scroll pHat
                            scrollphat.write_string("TrL")
                            DalekV2Drive.spinLeft(turnspeed)
                            time.sleep(.25)
                            DalekV2Drive.stop()
                        elif x > intXFrameCenter and panServoPosition <= 178:
                            panServoPosition = panServoPosition + 2
                            print "Turn Right: ", panServoPosition
                            scrollphat.clear()         # Shutdown Scroll pHat
                            scrollphat.write_string("TrR")
                            DalekV2Drive.spinRight(turnspeed)
                            time.sleep(.25)
                            DalekV2Drive.stop()
                        # end if else

                        if showcam == True:
                            # draw small green circle at center of detected object
                            cv2.circle(imgOriginal, (x, y), 3, (0, 255, 0), -1)
                            # draw red circle around the detected object
                            cv2.circle(imgOriginal, (x, y),
                                       radius, (0, 0, 255), 3)
                            # show windows
                            cv2.imshow("imgOriginal", imgOriginal)
                            cv2.imshow("imgThresh", imgThresh)
                        # end if
                    else:
                        panServoPosition = panServoPosition - 2
                        print "Turn Right: ", panServoPosition
                        scrollphat.clear()         # Shutdown Scroll pHat
                        scrollphat.write_string("TrR")
                        DalekV2Drive.spinRight(turnspeed)
                        time.sleep(.25)
                        DalekV2Drive.stop()
                        if showcam == True:
                            # show windows
                            cv2.imshow("imgOriginal", imgOriginal)
                            cv2.imshow("imgThresh", imgThresh)
                        # end if
                    # end if

#                    	if showcam == True:
#                        	cv2.imshow("imgOriginal", imgOriginal)                        # show windows
#                        	cv2.imshow("imgThresh", imgThresh)
#                     	end if

                # end while
            # end while
            # cv2.destroyAllWindows()

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
