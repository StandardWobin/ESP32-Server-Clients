
import copy
import time
import os
import numpy as np
import random
import math

class Design:
    def __init__(self, shared_data):
        self.shared_data = shared_data

        self.left_counter = 0
        self.right_counter = 0

        self.timer = {}
        self.timer["left"] = time.perf_counter()
        self.timer["right"] = time.perf_counter()
        self.timer["floating"] = time.perf_counter()

        self.counter = {}
        self.counter["left_top"] = 0
        self.counter["left_bot"] = 0
        self.counter["right_top"] = 0
        self.counter["right_bot"] = 0
        self.brain()


    def increase_light_led_strip(self, target = "", color = [255, 255, 255]):
        """if not audio_running:
                    self.shared_data["ap"].play_loading()
                    audio_running = True
        """   
        assert target in ["left_top", "left_bot", "right_top", "right_bot"]

        if target == "left_top":
            self.counter["left_bot"] = 0
        if target == "left_bot":
            self.counter["left_top"] = 0
        if target == "right_top":
            self.counter["right_bot"] = 0
        if target == "right_bot":
            self.counter["right_top"] = 0

        delta = time.perf_counter() - self.timer[target.split("_")[0]]
        self.timer[target.split("_")[0]] = time.perf_counter()

        self.counter[target] += delta * 75

        scale = min(int(self.counter[target])*3, len(self.shared_data["led_" + target.split("_")[0]])- 1)

        for i in range(len(self.shared_data["led_" + target.split("_")[0]])- 1):
            if i < scale:
                if i % 3 == 0:
                    self.shared_data["led_" + target.split("_")[0]][i] = color[0]
                if i % 3 == 1:
                    self.shared_data["led_" + target.split("_")[0]][i] = color[1]
                if i % 3 == 2:
                    self.shared_data["led_" + target.split("_")[0]][i] = color[2]
            else:
                if i % 3 == 0:
                    self.shared_data["led_" + target.split("_")[0]][i] = max(0, self.shared_data["led_" + target.split("_")[0]][i] - (self.shared_data["led_" + target.split("_")[0]][i]/10))
                if i % 3 == 1:
                    self.shared_data["led_" + target.split("_")[0]][i] = max(0, self.shared_data["led_" + target.split("_")[0]][i] - (self.shared_data["led_" + target.split("_")[0]][i]/10))
                if i % 3 == 2:
                    self.shared_data["led_" + target.split("_")[0]][i] = max(0, self.shared_data["led_" + target.split("_")[0]][i] - (self.shared_data["led_" + target.split("_")[0]][i]/10))



        # self.vanish_light_led_strip(target = target.split("_")[0], start = scale)


    

    def vanish_light_led_strip(self, target = "", start = 0):
        delta = time.perf_counter() - self.timer[target.split("_")[0]]
        self.shared_data["led_" + target][start:] = np.maximum([0]* len(self.shared_data["led_" + target][start:]), self.shared_data["led_" + target][start:] * (1-delta/20000000000))

    def make_floating(self, upper_bound=255, lower_bound=0, speed=0.1, dmx_pan_address = 2, dmx_tilt_address = 5):


        delta = (time.perf_counter() - self.timer["floating"]) * 1
        amp = math.sin(delta)

        x = self.interval_shift(amp, -1, 1, lower_bound, upper_bound)
        self.shared_data["dmx"][dmx_tilt_address] = (int)(x)   




        
        delta = (time.perf_counter() - self.timer["floating"]) * 0.1
        amp = math.sin(delta)

        x = self.interval_shift(amp, -1, 1, lower_bound, upper_bound)
        self.shared_data["dmx"][2] = (int)(x)    






    def interval_shift(self, x, a, b, c, d):
        assert a != b
        return c + ((d-c)/(b-a)) * (x -a )

            
    def evil_modus(self, speed_pan=1, speed_tilt=1, speed_strobe=1, color_speed=1, pan_bot=75, pan_top=85, tilt_bot=130, tilt_top=150, strobe_bot=70, strobe_top=248, color_bot=32, color_top=52):
        delta = (time.perf_counter() - self.timer["floating"])
        amp_tilt = math.sin(delta * speed_tilt) 
        amp_pan = math.sin(delta * speed_pan) 
        amp_strobe = math.sin(delta * speed_strobe) 
        amp_color = math.sin(delta * color_speed) 

        pan = self.interval_shift(amp_pan, -1, 1, pan_bot, pan_top)
        tilt = self.interval_shift(amp_tilt, -1, 1, tilt_bot, tilt_top)
        strobe = self.interval_shift(amp_strobe, -1, 1, strobe_bot, strobe_top)
        color = self.interval_shift(amp_color, -1, 1, color_bot, color_top)


        if abs(pan_bot - pan) > abs(pan_top - pan):
            pan = pan_top
        else:
            pan = pan_bot
   
        if abs(tilt_bot - tilt) > abs(tilt_top - tilt):
            tilt = tilt_top
        else:
            tilt = tilt_bot




        if abs(color_bot - color) > abs(color_top - color):
            color = color_top
        else:
            color = color_bot


        self.shared_data["dmx"][2] = (int)(pan)
        self.shared_data["dmx"][4] = (int)(tilt)
        self.shared_data["dmx"][8] = (int)(strobe)
        self.shared_data["dmx"][6] = (int)(color)







    def brain(self):
        global_counter = 0
        intense_counter = 20
        max_bright_ml = 50
        default_pan = 0
        default_tilt = 0

        # default tilt and pan
        ## self.shared_data["dmx"][2] = default_pan
        self.shared_data["dmx"][4] = default_tilt
        self.shared_data["dmx"][9] = 50



        self.shared_data["dmx"][3] = 126
        self.shared_data["dmx"][5] = 126


        self.shared_data["ap"].start_music()

        while 1:

            if any(self.shared_data["taster_activation_left"]) or any(self.shared_data["taster_activation_right"]):
                self.shared_data["ap"].play_loading()
            else:
                self.shared_data["ap"].stop_loading()

            # #####################################################################
            # #####################################################################
            # #####################################################################
            # #####################################################################
            ## LEFT
            # press A on the left board
            if self.shared_data["taster_activation_left"][0] == 1:
                self.increase_light_led_strip(target = "left_top", color = [116, 26, 0])

            # press B on the left board
            elif self.shared_data["taster_activation_left"][1] == 1:
                self.increase_light_led_strip(target = "left_top", color = [116, 26, 0])

            # press C on the left board
            elif self.shared_data["taster_activation_left"][2] == 1:
                self.increase_light_led_strip(target = "left_bot", color = [0, 0, 255])

            # press D on the left board
            elif self.shared_data["taster_activation_left"][3] == 1:
                self.increase_light_led_strip(target = "left_bot", color = [0, 0, 255])

                 
            elif not any(self.shared_data["taster_activation_left"]):
                ## no press on any key
                # if audio_running:
                #    self.shared_data["ap"].stop_loading()
                #    audio_running = False
                self.counter["left_top"] = 0
                self.counter["left_bot"] = 0

                self.timer["left"] = time.perf_counter()

                self.vanish_light_led_strip("left")




            # #####################################################################
            # #####################################################################
            # #####################################################################
            # #####################################################################
            ## Right
            # press A on the left board
            if self.shared_data["taster_activation_right"][0] == 1:
                self.increase_light_led_strip(target = "right_top", color = [116, 26, 0])

                   
            # press B on the left board
            elif self.shared_data["taster_activation_right"][1] == 1:
                self.increase_light_led_strip(target = "right_top", color = [116, 26, 0])

               

            elif self.shared_data["taster_activation_right"][2] == 1:
                self.increase_light_led_strip(target = "right_bot", color = [0, 0, 255])

                #if not audio_running:
                #   self.shared_data["ap"].play_loading()
                #   audio_running = True

            elif self.shared_data["taster_activation_right"][3] == 1:
                self.increase_light_led_strip(target = "right_bot", color = [0, 0, 255])

                #if not audio_running:
                #   self.shared_data["ap"].play_loading()
                #   audio_running = True
                 

            elif not any(self.shared_data["taster_activation_right"]):
                ## no press on any key
                # if audio_running:
                #    self.shared_data["ap"].stop_loading()
                #    audio_running = False
                self.counter["right_top"] = 0
                self.counter["right_bot"] = 0

                self.timer["right"] = time.perf_counter()

                self.vanish_light_led_strip("right")




            left_full = sum(self.shared_data["led_left"][-4:-1]) > 0
            right_full = sum(self.shared_data["led_right"][-4:-1]) > 0

            orange_block = any(self.shared_data["taster_activation_left"][0:1]) and any(self.shared_data["taster_activation_right"][0:1])
            blue_block = any(self.shared_data["taster_activation_left"][2:3]) and any(self.shared_data["taster_activation_right"][2:3])


            # BLOCK BLOCK BLOCK
            if left_full and right_full and (orange_block or blue_block):
                # enter the void all pressed and full

                self.evil_modus(speed_pan=6, speed_tilt=6, speed_strobe=1, color_speed=2.3)
                self.shared_data["dmx"][1] = 0
                self.shared_data["motor"] = 0

                self.shared_data["ap"].set_evil(True)

                continue
            else: 
                # self.shared_data["dmx"][2] = default_pan


                self.shared_data["ap"].set_evil(False)


            if left_full and self.shared_data["taster_activation_left"][0] == 1:
                self.shared_data["motor"] = 1
                self.shared_data["dmx"][6] = 57
                self.shared_data["dmx"][2] = 141
                self.shared_data["dmx"][4] = 16
                print("oeben links")
            
            elif left_full and self.shared_data["taster_activation_left"][1] == 1:
         
                self.shared_data["motor"] = -1

                self.shared_data["dmx"][6] = 57
                self.shared_data["dmx"][2] = 141
                self.shared_data["dmx"][4] = 16
                print("unten links")




            elif left_full and self.shared_data["taster_activation_left"][2] == 1:
     

                self.shared_data["dmx"][1] = 1
                self.shared_data["dmx"][6] = 38
                self.shared_data["dmx"][2] = 230
                self.shared_data["dmx"][4] = 31
                print("oben rehtcs")

      
                
            elif left_full and self.shared_data["taster_activation_left"][3] == 1:
                self.shared_data["dmx"][1] = 255
                self.shared_data["dmx"][6] = 38
                self.shared_data["dmx"][2] = 230
                self.shared_data["dmx"][4] = 31
                print("unten rehtcs")








            # WHEEL ORANGE
            elif right_full and self.shared_data["taster_activation_right"][0] == 1:
                self.shared_data["motor"] = -1

                self.shared_data["dmx"][6] = 57
                self.shared_data["dmx"][2] = 141
                self.shared_data["dmx"][4] = 16
                print("ORANGE WHHEL RECHTS")

            elif right_full and self.shared_data["taster_activation_right"][1] == 1:
                self.shared_data["motor"] = 1

                self.shared_data["dmx"][6] = 57
                self.shared_data["dmx"][2] = 141
                self.shared_data["dmx"][4] = 16
                print("ORANGE WHHEL Right")


                # MOBILE BLAU
            elif right_full and self.shared_data["taster_activation_right"][2] == 1:
                self.shared_data["dmx"][1] = 255
                self.shared_data["dmx"][6] = 38
                self.shared_data["dmx"][2] = 230
                self.shared_data["dmx"][4] = 31
                print("wh BLAU RECHTS")

            elif right_full and self.shared_data["taster_activation_right"][3] == 1:
                self.shared_data["dmx"][1] = 1
                self.shared_data["dmx"][6] = 38
                self.shared_data["dmx"][2] = 230
                self.shared_data["dmx"][4] = 31
                print("RECHS BLAU")


            else:
                ## nothing pressed nothing full
                self.shared_data["dmx"][1] = 0
            
                self.shared_data["dmx"][4] = default_tilt
                self.shared_data["dmx"][9] = 30
                self.shared_data["dmx"][6] = 0
                self.shared_data["dmx"][8] = 0
                self.shared_data["motor"] = 0
                self.shared_data["dmx"][8] = 0
                self.make_floating(speed=0.1)
            
            

   

      





            """
            # line reaches end
           
            """
