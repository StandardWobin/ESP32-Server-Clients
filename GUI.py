import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import Canvas
from tkinter import Button


from tkinter.ttk import Progressbar
from tkinter import ttk
import copy

import os


class GUI:
    def __init__(self, shared_data):






        self.master = tk.Tk()
        self.master.title("E-VOTE MASTER")
        self.width = 1680
        self.height = 1200
        self.master.geometry(str(self.width) + "x" + str(self.height))

        self.shared_data = shared_data

        style = ttk.Style()

        ## Progressbar
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='black')
        self.p_bar = Progressbar(self.master, length=200, style='black.Horizontal.TProgressbar')
        self.p_bar.grid(row=1, column=1)
        self.p_bar_left_label = tk.Label(self.master, text="0", font=("Arial Bold", 12),  anchor="e")
        self.p_bar_right_label = tk.Label(self.master, text="0", font=("Arial Bold", 12))
        self.p_bar_top_label = tk.Label(self.master, text="votings", font=("Arial Bold", 12))
        self.p_bar_left_label.grid(row=1, column=0, sticky="e")
        self.p_bar_right_label.grid(row=1, column=2)
        self.p_bar_top_label.grid(row=0, column=1)
        self.clients = {}



        self.other3 = tk.Label(self.master, background="pink")
        self.other4 = tk.Label(self.master, background="pink")

        self.other3.grid(row=2, column=0, sticky="nsew")
        self.other4.grid(row=2, column=1, sticky="nsew")


        self.output = scrolledtext.ScrolledText(self.master,
                            bg='white',
                            relief="sunken",
                            height=20,
                            #width=400,
                            font='TkFixedFont',)
        self.output.grid(row = 50, column = 0, columnspan=4, sticky="N")


        self.draw_to_infinity()

    def draw_to_infinity(self):
        i = 0
        while True:
            self.master.update_idletasks()
            self.master.update()
            self.update_clients()

    def to_output(self, m):
        self.output.insert(tk.END, "\n" + m)
        self.output.see("end")

    def update_clients(self):
        keys = self.shared_data.keys()
        client_keys = self.clients.copy().keys()
        update = []

        for k in keys:
            if "client_state" in k:
                update.append(k)
        counter = 0

        for up in update:
            name = up.split("_")[2]

            if up in client_keys:
                ## we already have the client!
                # print("known client")


                """ Traceback (most recent call last):
                File "/usr/lib/python3.7/threading.py", line 926, in _bootstrap_inner
                    self.run()
                File "/usr/lib/python3.7/threading.py", line 870, in run
                    self._target(*self._args, **self._kwargs)
                File "Socketserver.py", line 30, in thread_function_gui
                    gui = GUI(shared_information)
                File "/home/rob/Documents/Server/GUI.py", line 64, in __init__
                    self.draw_to_infinity()
                File "/home/rob/Documents/Server/GUI.py", line 71, in draw_to_infinity
                    self.update_clients()
                File "/home/rob/Documents/Server/GUI.py", line 106, in update_clients
                    temp.update_state(self.shared_data[up], "", self.shared_data["client_activation_"+ name])
                KeyError: 'client_activation_' """


                self.clients[up].update_state(self.shared_data[up], self.shared_data["client_msgs_"+ name], self.shared_data["client_activation_" + name])

                self.shared_data["client_led_"+ name] = self.clients[up].led

                if self.clients[up].outval.get() == 1:
                    if self.clients[up].last_message is not self.shared_data["client_msg_" + name]:
                        self.to_output(name + " recieved: " + self.shared_data["client_msg_" + name])
                        self.clients[up].last_message =  self.shared_data["client_msg_" + name]

            else:
                self.to_output("new client: " + name)
                temp = ClientUI(self.master, up.split("_")[2])
                temp.grid(row=((len(client_keys)+counter) // 3)+3, column=((len(client_keys)+counter) % 3), sticky="ew", padx=(10, 10), pady=(10,10))
                temp.update_state(self.shared_data[up], "", self.shared_data["client_activation_"+ name])
                self.clients[up] = temp
                counter = +1

            ## check if we already have a box
                


    def warning(self, m):
        messagebox.showwarning('Warning', m)  #shows warning message


    def error_message(self, m):   
        messagebox.showwarning('Error', m)  #shows warning message


    def update_progressbar(self, value, max, left="", right="", top=""):
        if len(left)>0:
            self.p_bar_left_label.setvar(left)
        if len(right)>0:
            self.p_bar_right_label.setvar(right)
        if len(top)>0:
            self.p_bar_top_label.setvar(top)

        percent = value/max*100
        self.p_bar['value'] = percent



class ClientUI(tk.Frame):
    def toggle(self):
        print("toggles")
        self.led = not self.led

    def __init__(self, parent, label, default=""):
        tk.Frame.__init__(self, parent)


        self.global_border = tk.Frame(master=self, background='snow', borderwidth=2, relief="groove")     
        self.global_border.pack(side='top', fill="x") 



        self.name = tk.Label(self.global_border, text=label, anchor="center", background='snow')
        self.name.pack(side="top", fill="x")

        self.status = tk.Label(self.global_border, text="status", anchor="w", background='snow')
        self.status.pack(side="top", fill="x")

        self.border = tk.Frame(self.global_border, background='yellow')     
        self.border.pack(side='top', fill="x", padx="3") 

        self.msg = tk.Label(self.border, text="msg/s = " + str(0), anchor="w")
        self.msg.pack(side="top",  padx='5', pady='5')



        self.poll = tk.Label(self.global_border, text="Poll", anchor="w", background='snow')
        self.poll.pack(side="top", fill="x")



        self.border2 = tk.Frame(self.global_border)     
        self.border2.pack(side='top', padx='5', pady='5', fill="x") 

        self.status = []
        for i in range(8):
            self.status.append(tk.Label(self.border2, text="", anchor="center", background="black", width=2, height=1))
            self.status[i].pack(side="left", padx='5', pady="1")


        self.border3 = tk.Frame(self.global_border)     
        self.border3.pack(side='top', padx='5', pady='5', fill="x") 

        self.led = False
        self.button = Button(self.border3, text="LED", command=self.toggle)
        self.button.pack(side="left")

        self.pollval = tk.IntVar()
        c1 = tk.Checkbutton(self.border3, text='Poll',variable=self.pollval, onvalue=1, offvalue=0, anchor="center")
        c1.pack(side="left")


        self.last_message = ""

        self.outval = tk.IntVar()
        c1 = tk.Checkbutton(self.border3, text='output',variable=self.outval, onvalue=1, offvalue=0, anchor="center")
        c1.pack(side="right")


        self.update_state(0, "", [0] * 8)



    def update_state(self, state, text, activations):

        
        if self.led:
            self.button["text"] = "LED:on"
        else:
            self.button["text"] = "LED:off"


        self.state = state
        if self.state == 0:
            self.msg["bg"] = "red"
            self.border["bg"] = "red"
        elif self.state == 1:
            self.msg["bg"] = "orange"
            self.border["bg"] = "orange"
        elif self.state == 2:
            self.msg["bg"] = "green"
            self.border["bg"] = "green"

        self.msg["text"] = "msg/s = " + str(text)

        for act_ix, act in enumerate(activations):
            if act == 1:
                self.status[act_ix]["background"] = "green"
            else:
                self.status[act_ix]["background"] = "black"


    def get(self):
        return self.entry.get()









