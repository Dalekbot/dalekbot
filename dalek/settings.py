class Settings():

    
    speed = 50               # 0 is stopped, 100 is fastest
    right_speed = 50          # 0 is stopped, 100 is fastest
    left_speed = 50           # 0 is stopped, 100 is fastest
    max_speed = 100           # Set full Power
    min_speed = 0             # Set min power  
    inner_turn_speed = 40      # Speed for Inner Wheels in a turn
    outer_turn_speed = 80      # Speed for Outer Wheels in a turn
    hRes = 640               # PiCam Horizontal Resolution
    vRes = 480               # PiCam Vertical Resolution
    camera = 0               # Create PiCamera Object
    video_capture = 0        # Create WebCam Object
    show_cam = False         # if the camera image is shown to screen of not 
    sound_volume = 0          # Set Default Sound Volume -15 - 10


    def __init__(self):
      pass
    def debug_print(self):
      print("speed:{}".format(self.speed))
      print("right_speed:{}".format(self.right_speed))
      print("left_speed:{}".format(self.left_speed))
      print("max_speed:{}".format(self.max_speed))
      print("min_speed:{}".format(self.min_speed))
      print("inner_turn_speed:{}".format(self.inner_turn_speed))
      print("outer_turn_speed:{}".format(self.outer_turn_speed))
      print("hRes:{}".format(self.hRes))
      print("vRes:{}".format(self.vRes))
      print("camera:{}".format(self.camera))
      print("video_capture:{}".format(self.video_capture))
      print("show_cam:{}".format(self.show_cam))
      print("sound_volume:{}".format(self.sound_volume))
      

def main():
    x1 = Settings()
    print(x1.debug_print())


if __name__ == "__main__":
  main()
    