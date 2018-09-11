 ###############################################
  ###  Main Paddle controls on ps3 controller  ##
  ###############################################
  # def paddleControl(aX, aY,minusX, minusY):
      
  
  #     v_speed =  aY
  #     alog1 = aX/10
  #     if alog1>0:
  #       v_speed2 = v_speed/alog1
  #     else:
  #       v_speed2=1
      
  #     v_speed_3= aY
  #     alog2 = aX/5
  #     if alog2 > 0:
  #       v_speed_3 = alog2
  #     else:
  #       v_speed_3=1
    
  #     DalekPrint( 'ax:{}  aY:{} v_speed{} v_speed2 {}' .format(aX,aY , v_speed, v_speed2) )
  
  #     DalekPrint('v_speed: %s' % v_speed )
     
     
  #     # Paddle moved center
  #     if aY == 0 and aX ==0:
  #       dalek_drive.stop()
  #       DalekPrint("Stop","STP")
      
  #     #-------------------------------------
  #     # up movements
  
  #     # Paddle moved up only
  #     elif minusY  and aX == 0: 
  #       dalek_drive.forward(v_speed)
  #       DalekPrint("forward - {}".format(v_speed), "FW")
  
  #     # turnForwardRight
  #     elif minusY and minusX:
        
  #       if aY >50:
  
  #         dalek_drive.paddleForward(v_speed2, v_speed)
  #         DalekPrint('paddleForward turn right', "PTR")
  #       else:
  #         # dalek_drive.turnForwardLeft(v_speed, v_speed_3)
  #         dalek_drive.paddleForward(v_speed_3, v_speed)
  #         DalekPrint('paddleForward turn right',"PTR")
  #     # turnForwardLeft
  #     elif minusY and minusX == False:
        
  #       if aY > 50:
  #         dalek_drive.paddleForward( v_speed, v_speed2)
  #         # dalek_drive.turnBackwardRight(v_speed_3,v_speed)
  #         DalekPrint('turn right',"TR")
  #       else:
  #         dalek_drive.paddleForward( v_speed, v_speed_3)
  #         # dalek_drive.turnForwardRight(v_speed_3,v_speed)
  
  #     #-------------------------------------
  #     # spin movements
  
  #     #spin Left
  #     elif aY==0 and minusX :
  #       dalek_drive.spinLeft(aX)
      
  #     #spin Right
  #     elif aY==0 and minusX == False :
  #       dalek_drive.spinRight(aX)
  # #-------------------------------------
  # # Down movements
  #     # Paddle moved down only
  #     elif minusY == False and aX == 0:
  #       dalek_drive.backward(v_speed)
  #       DalekPrint("backwards - {}".format(v_speed), "BW")
  
  #     # backwards right
  #     elif minusY== False and minusX == False:
        
  #       dalek_drive.paddleBackward( v_speed, v_speed2)
  #       DalekPrint('turn right', "TR")
  #     # backwards left 
  #     elif minusY== False and minusX == True:
       
  #       dalek_drive.paddleBackward( v_speed2, v_speed)
  #       DalekPrint('turn right', "TR") 
