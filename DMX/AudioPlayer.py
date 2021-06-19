#!/usr/bin/env python3
# Import playsound module
from playsound import playsound
import multiprocessing
import time
# importing vlc module
import vlc
import random


class AudioPlayer:
    def __init__(self):
        self.loading_sound = "./audios/DunDun.wav"
        self.loading_interrupt_sound = "./audios/DunDun-Fast.wav"
        self.blocking_sound = "./audios/zelda.mp3"
        self.loading_process = None
        self.blocking_process = None
        self.music_process = None

        self.manager = multiprocessing.Manager()
        self.speed = self.manager.Value("speed", 1)
        self.evil = self.manager.Value("evil", False)






    def set_music_speed(self, speed=1):
        assert speed > 0 and speed < 5
        self.speed.value = speed


    def set_evil(self, evil=False):
        self.evil.value = evil




    def start_music(self):
        if self.music_process is None:
            self.music_process = multiprocessing.Process(target=self.music_helper, args=(self.speed, self.evil))
            self.music_process.start()
        else:
            print("you can only start the music once!")
            assert 1 == 0

    def music_helper(self, speed, evil):
        song = vlc.Media("./audios/hannah.mp3")

        player = vlc.MediaPlayer()

        player.set_media(song)
        player.audio_set_delay(1)

        

        player.play()
        while 1:
            player.set_rate(speed.value)
            time.sleep(0.1)
            start = player.get_position()
            hit = False
            while (evil.value):
                time.sleep(random.uniform(0.001, 0.4))
                player.set_position(max(0, min(1, start+random.uniform(-0.01, +0.01))))
                hit = True

            if not evil.value:
                if hit:
                    player.set_position(start)





    def stop_music(self):


        if self.music_process.is_alive():
            # _ = multiprocessing.Process(target=playsound, args=(self.loading_interrupt_sound,))
            # _.start() 
            self.music_process.terminate()

    def play_blocking(self):
        self.blocking_process = multiprocessing.Process(target=playsound, args=(self.blocking_sound,))
        self.blocking_process.start()

    def stop_blocking(self):
        if self.blocking_process.is_alive():
            self.blocking_process.terminate()

    def play_loading(self):
        if self.loading_process is None:
            self.loading_process = multiprocessing.Process(target=playsound, args=(self.loading_sound,))
            self.loading_process.start()

    def stop_loading(self):      
        if self.loading_process is not None:
            if self.loading_process.is_alive():
                # _ = multiprocessing.Process(target=playsound, args=(self.loading_interrupt_sound,))
                # _.start() 
                self.loading_process.terminate()
            self.loading_process = None

       



if False:
    ap = AudioPlayer()
    ap.start_music()
    time.sleep(5)
    ap.set_evil(True)
    time.sleep(3)
    ap.set_evil(False)
    time.sleep(3)

    while 1:
        pass
