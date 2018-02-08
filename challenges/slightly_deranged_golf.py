# if __name__ == "__main__":
#    '''
#    This if statement is needed for testing, to locate the modules needed
#    if we are running the file directly.
#    '''
#    import sys
#    from os import path
#    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
#    from dalek import settings
#    from dalek import sound_player
#    import RPi.GPIO as GPIO

# these are the globaly used modules
from challenges import challenge
import time
# from dalek import spi
# from dalek import drive
from dalek import debug


class Challenge(challenge.ChallengeBase):
    '''
    Do Not change the class name, it is called in the controller.py.
    The buttons can be overridden if you need to add functionally to them.
    The main loop is the run() function, all code goes in it.

    Look at the ChallengeBase class in challenge.py for all functions that can be called.
    '''

    def __init__(self, dalek_settings, dalek_sounds):
        super().__init__()
        self.dalek_settings = dalek_settings
        self.dalek_sounds = dalek_sounds

    def run(self):
        self.running = True
        debug.print_to_all_devices(
            "Challenge 'slightly_deranged_golf' Started.")
        while self.running:

            ####################################################
            #                                                  #
            # Code for this challange goes in this while loop  #
            #                                                  #
            ####################################################
            debug.print_to_all_devices("Putt! ")  # this line can be removed
            # this line can be removed
            time.sleep(2)


def main(dalek_settings, dalek_sounds):
    pass
    # challenge = Challenge(dalek_settings, dalek_sounds)
    # challenge.start()
    # time.sleep(4)
    # challenge.button_circle_pressed()
    # challenge.stop_runnning()

    # challenge.join() # wait for thead to finish.
    # debug.print_to_all_devices("\nFINISHED")


if __name__ == "__main__":
    pass
    # debug.debug_on = True
    # dalek_settings = settings.Settings()
    # dalek_sounds = sound_player.Mp3Player(True) # initialize the sound player
    # main(dalek_settings, dalek_sounds)

else:
    debug.print_to_all_devices('importing slightly_deranged_golf Challenge')
