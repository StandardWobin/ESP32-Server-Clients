import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import Canvas
from tkinter import Button
from tkinter import Scale
from tkinter import Label



from tkinter.ttk import Progressbar
from tkinter import ttk
import copy

import os


class GUI:
    def __init__(self, shared_data):






        self.master = tk.Tk()
        self.master.title("DMX")
        self.width = 1850
        self.height = 400
        self.master.geometry(str(self.width) + "x" + str(self.height))

        self.shared_data = shared_data

        style = ttk.Style()

        ## Progressbar


        self.clients = {}
        self.scales = []

        self.start = 0
        for y in range(3):
            temp_border = Label(master=self.master, background='snow', borderwidth=2, relief="groove")     
            temp_border.pack(side='top', fill="x", ) 

            for i in range(25):
                temp_border2 = Label(master=temp_border, background='snow', borderwidth=2, relief="groove")     
                temp_border2.pack(side='left', fill="x") 


                if i in range(25) and y == 0:
                    if i == 0:
                        text = "MASTER"
                    elif i == 1:
                        text = "M:motor"
                    elif i == 2:
                        text = "ML:pan x"
                    elif i == 3:
                        text = "ML:cor x"
                    elif i == 4:
                        text = "ML:tilt y"
                    elif i == 5:
                        text = "ML:cor y"
                    elif i == 6:
                        text = "ML:color"
                    elif i == 7:
                        text = "ML:gobo"
                    elif i == 8:
                        text = "ML:strobo"
                    elif i == 9:
                        text = "ML:vol"
                    elif i == 10:
                        text = "ML:?"
                    elif i == 11:
                        text = "ML:party"
                    elif i == 12:
                        text = "ML:aut-pan"
                    elif i == 13:
                        text = "LED1:vol-R"
                    elif i == 14:
                        text = "LED1:x-R"
                    elif i == 15:
                        text = "LED1:vol-G"
                    elif i == 16:
                        text = "LED1:x-G"
                    elif i == 17:
                        text = "LED1:vol-B"
                    elif i == 18:
                        text = "LED1:x-B"
                    elif i == 19:
                        text = "LED2:vol-R"
                    elif i == 20:
                        text = "LED2:x-R"
                    elif i == 21:
                        text = "LED2:vol-G"
                    elif i == 22:
                        text = "LED2:x-G"
                    elif i == 23:
                        text = "LED2:vol-B"
                    elif i == 24:
                        text = "LED2:x-B"



                    else:
                        text = str(i + y*25)

                else:
                    text = str(i + y*25)
                label = Label(master=temp_border2, background='snow', text=text, borderwidth=2, width=8,  relief="groove")     
                label.pack(side='top', fill="x") 
                _ = Scale(temp_border2, from_=255, to=0)
                _.pack(side="top")
                self.scales.append(_)





        self.draw_to_infinity()

    def draw_to_infinity(self):
        i = 0
        self.led1_red_vol = 0
        self.led1_green_vol = 0
        self.led1_blue_vol = 0
        self.led2_red_vol = 0
        self.led2_green_vol = 0
        self.led2_blue_vol = 0
        self.global_master = 0
        while True:
            self.master.update_idletasks()
            self.master.update()
            self.update_dmx()


    def update_dmx(self):
        for s_ix, s in enumerate(self.scales):
            if s_ix == 0:
                self.global_master = (s.get()/255) 

            elif s_ix == 9:
                self.shared_data["dmx"][self.start + s_ix] = (int)(s.get() * self.global_master)

            elif s_ix == 13:
                self.led1_red_vol = s.get()
            elif s_ix == 14:
                for i in range(0, 450, 3):
                    if i <= s.get():
                        self.shared_data["led_left"][i] = (int)(self.led1_red_vol * self.global_master)
                    else:
                        self.shared_data["led_left"][i] = 0
            elif s_ix == 15:
                self.led1_green_vol = s.get()
            elif s_ix == 16:
                for i in range(1, 450, 3):
                    if i <= s.get():
                        self.shared_data["led_left"][i] = (int)(self.led1_green_vol * self.global_master)
                    else:
                        self.shared_data["led_left"][i] = 0
            elif s_ix == 17:
                self.led1_blue_vol = s.get()
            elif s_ix == 18:
                for i in range(2, 450, 3):
                    if i <= s.get():
                        self.shared_data["led_left"][i] = (int)(self.led1_blue_vol * self.global_master)
                    else:
                        self.shared_data["led_left"][i] = 0
            elif s_ix == 19:
                self.led2_red_vol = s.get()
            elif s_ix == 20:
                for i in range(0, 450, 3):
                    if i <= s.get():
                        self.shared_data["led_right"][i] = (int)(self.led2_red_vol * self.global_master)
                    else:
                        self.shared_data["led_right"][i] = 0
            elif s_ix == 21:
                self.led2_green_vol = s.get()
            elif s_ix == 22:
                for i in range(1, 450, 3):
                    if i <= s.get():
                        self.shared_data["led_right"][i] = (int)(self.led2_green_vol * self.global_master)
                    else:
                        self.shared_data["led_right"][i] = 0
            elif s_ix == 23:
                self.led2_blue_vol = s.get()
            elif s_ix == 24:
                for i in range(2, 450, 3):
                    if i <= s.get():
                        self.shared_data["led_right"][i] = (int)(self.led2_blue_vol * self.global_master)
                    else:
                        self.shared_data["led_right"][i] = 0
       
            elif s_ix == 25:
                    if s.get() < 100:
                        self.shared_data["motor"] = -1
                    elif s.get() < 200:
                        self.shared_data["motor"] = 0
                    else:
                        self.shared_data["motor"] = 1

       
            else:
                self.shared_data["dmx"][self.start + s_ix] = s.get() 

    def warning(self, m):
        messagebox.showwarning('Warning', m)  #shows warning message


    def error_message(self, m):   
        messagebox.showwarning('Error', m)  #shows warning message





    def get(self):
        return self.entry.get()









