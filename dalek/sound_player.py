#!/usr/bin/env python
import subprocess


# uses MPlayer 1.3.0

class Mp3Player():
    """
       Plays a sounds with  mplayer  (it needs to be installed
       on the device first.)

       play_sound() - omit the folder and .mp3 extention
       set_volume_level()
       increese_volume_level()
       decreese_volume_level()
       mute_sound()
       un_mute_sound()
    """
    volume_level = 0
    temp_volume_level = 0

    __max_volume_level = 10
    __min_volume_level = -20

    def __init__(self, is_sound_on=True, volume_level=0):
        if is_sound_on == True:
            self.is_sounds_on = True
        else:
            self.is_sounds_on = False

        self.volume_level = volume_level

    def set_volume_level(self, volume_level):
        # volume_level is between min and max
        if self.__min_volume_level <= volume_level <= self.__max_volume_level:
            self.volume_level = volume_level
            print("volume_level:{}".format(self.volume_level))

    def increese_volume_level(self):
        if (self.volume_level + 1) < self.__max_volume_level:
            self.volume_level += 1
            print("volume_level:{}".format(self.volume_level))

    def decreese_volume_level(self):
        if self.volume_level > self.__min_volume_level:
            self.volume_level -= 1
            print("volume_level:{}".format(self.volume_level))

    def mute_sound(self):
        self.temp_volume_level = self.set_volume_level
        self.is_sounds_on = False
        self.sound_volume = 0

    def un_mute_sound(self):
        self.set_volume_level = self.temp_volume_level
        self.is_sounds_on = True

    def play_sound(self, mp3_to_play):
        # omit the folder and .mp3 file type. The files should be in the Sounds folder
        volumesetting = "volume={}".format(self.volume_level)
        file_to_play = "./sounds/{}.mp3".format(mp3_to_play)
        try:
            subprocess.Popen(["mplayer", file_to_play, '-af', volumesetting],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,  stderr=subprocess.PIPE)

        except expression as identifier:
            print("sound player error.")


def main():
    print("dalek_sound_player")
    x = PlaySound()
    x.set_volume_level(-5)
    x.play_sound("Beginning")
    time.sleep(4)
    print("done")


if __name__ == '__main__':
    import time
    main()
