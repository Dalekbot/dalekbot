#from glob import glob
#import itertools as it
#import struct

#from imutils.object_detection import non_max_suppression
#from imutils import paths

#======================================================================
# Service Procedures
def updateServoMotorPositions(pwm, panServoPosition, tiltServoPosition):
    panDutyCycle = ((float(panServoPosition) * 0.3) + 15) * 10
    tiltDutyCycle = ((float(tiltServoPosition) * 0.1555556) + 20) * 10
    
    #pwmPanObject.ChangeDutyCycle(panDutyCycle)
    pwm.setPWM(servoHorizontalPort, 0, int(panDutyCycle))
    #pwmTiltObject.ChangeDutyCycle(tiltDutyCycle)
    pwm.setPWM(servoVerticalPort, 0, int(tiltDutyCycle))
# end function
    
# End of Service Procedures    
#======================================================================


# use Arduino Instead 
def getdistance(distance, TRIG, ECHO):
    GPIO.output(TRIG, False)
    #print "Waiting For Sensor To Settle"
    time.sleep(0.05)
    pulse_start = 0
    pulse_end = 0

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        #print 'start', GPIO.input(ECHO)
        pulse_start = time.time()
  
    while GPIO.input(ECHO)==1:
        #print 'stop', GPIO.input(ECHO)
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    #print "Distance:",distance,"cm"
    return distance


  # ---- Function definition for converting scales ------
def remap(unscaled, to_min, to_max, from_min, from_max):
    return (to_max-to_min)*(unscaled-from_min)/(from_max-from_min)+to_min
    
def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh



#def draw_detections(img, rects, thickness = 1):
#    # pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
#    for x, y, w, h in rects:
#        # the HOG detector returns slightly larger rectangles than the real objects.
#        # so we slightly shrink the rectangles to get a nicer output.
#        pad_w, pad_h = int(0.15*w), int(0.05*h)
#        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)
#    # end for
#    return