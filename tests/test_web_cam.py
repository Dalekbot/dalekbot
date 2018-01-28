import cv2 
import time

hRes = 640               # PiCam Horizontal Resolution
vRes = 480               # PiCam Virtical Resolution
camera = 0 

video= cv2.VideoCapture(0)

video.set(3, hRes)
video.set(4, vRes)
a=0

while True:
  
    ret, frame = video.read()
    
    # print(check)
    # print(frame)
    
    # Crop, select part of image to work with
    crop_img = frame[380:480, 0:640]

    cx = 300 
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # Apply a Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)
    # Apply Color thresholding
    ret,thresh = cv2.threshold(blur,100,255,cv2.THRESH_BINARY_INV)
    
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

    cv2.imshow('frame',crop_img)
    key = cv2.waitKey(1)
    if key == ord('q'):
      break

video.release()
cv2.destroyAllWindows()

