if __name__ == "__main__":
    '''
    This if statement is needed for testing, to locate the modules needed
    if we are running the file directly.
    '''
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
   #  from dalek import settings
   #  from dalek import sound_player
    import RPi.GPIO as GPIO          # Import GPIO divers

import time
# from dalek import spi
from dalek import drive
from dalek import debug
import threading


# it needs to run in a thread otherwise the joystick can not run at the same time


class ChallengeBase(threading.Thread):
    '''
    This class is used as a interface for all challenges. 
    If you need to change functionality then override it in 
    the calling class.
    '''

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        self.running = True
        print("challenge template class is running You need to override the run(self) function")
        while self.running:

            ####################################################
            #                                                  #
            # Code for this challenge goes in this while loop  #
            #                                                  #
            ####################################################
            # this line can be removed
            debug.print_to_all_devices("challenge base class !!")
            time.sleep(2)                         # this line can be removed

    def stop_running(self):
        '''
        When this is called it ends this thread 
        This is also called if the PS3 button is pressed during a challenge,
        so add any cleanup code here.
        '''
        drive.stop()
        self.running = False
        debug.print_to_all_devices("Done...")

    ####################################
    #           BUTTONS                #

    def button_cross_pressed(self):
        debug.print_to_all_devices(
            "x_button_pressed() in challenges/ChallengeBase class")

    def button_cross_released(self):
        debug.print_to_all_devices(
            "x_button_released() in challenges/ChallengeBase class")

    def button_circle_pressed(self):
        debug.print_to_all_devices(
            "circle_button_pressed() in challenges/ChallengeBase class")

    def button_circle_released(self):
        debug.print_to_all_devices(
            "circle_button_released() in challenges/ChallengeBase class")

    def button_triangle_pressed(self):
        debug.print_to_all_devices(
            "triangle_button_pressed() in challenges/ChallengeBase class")

    def button_triangle_released(self):
        debug.print_to_all_devices(
            "triangle_button_released() in challenges/ChallengeBase class")

    def button_square_pressed(self):
        debug.print_to_all_devices(
            "square_button_pressed() in challenges/ChallengeBase class")

    def button_square_released(self):
        debug.print_to_all_devices(
            "square_button_released() in challenges/ChallengeBase class")

    def button_L1_pressed(self):
        debug.print_to_all_devices(
            "L1_pressed() in challenges/ChallengeBase class")

    def button_L1_released(self):
        debug.print_to_all_devices(
            "L1_released() in challenges/ChallengeBase class")

    def button_L2_pressed(self):
        debug.print_to_all_devices(
            "L2_pressed() in challenges/ChallengeBase class")

    def button_L2_released(self):
        debug.print_to_all_devices(
            "L2_released() in challenges/ChallengeBase class")

    def button_R1_pressed(self):
        debug.print_to_all_devices(
            "R1_pressed() in challenges/ChallengeBase class")

    def button_R1_released(self):
        debug.print_to_all_devices(
            "R1_released() in challenges/ChallengeBase class")

    def button_R2_pressed(self):
        debug.print_to_all_devices(
            "R2_pressed() in challenges/ChallengeBase class")

    def button_R2_released(self):
        debug.print_to_all_devices(
            "R2_released() in challenges/ChallengeBase class")


def main():
    challenge = ChallengeBase()
    challenge.start()
    challenge.join()  # wait for thread to finish.
    debug.print_to_all_devices("\nFINISHED")


if __name__ == "__main__":
    debug.debug_on = True
    # dalek_settings = settings.Settings()
    # dalek_sounds = sound_player.Mp3Player(True) # initialize the sound player
    main()

else:
    debug.print_to_all_devices('Challenge Base')
