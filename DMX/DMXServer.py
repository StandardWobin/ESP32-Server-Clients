
# import socket programming library 
import socket 
  
import math
import sys  
# import thread module 
import threading 
import select
from GUI import GUI
from Design import Design
from AudioPlayer import AudioPlayer
import numpy as np

print_lock = threading.Lock() 
  
import time  
# thread function 

def thread_function_gui(shared_data):
    print("thead startest für hui")
    gui = GUI(shared_data)
    

def thread_function_design(shared_data):
    print("thead startest für hui")
    design = Design(shared_data)


def thread_function_sockets(data):
    c = data[0]
    avg_msg_recv_counter = 0
    msg_sent_counter = 0
    msg_recv_counter = 0
    threadnumber = data[1] 
    shared_data = data[2]

    print("******************************************")
    print("THREAD " + str(threadnumber) + " INITIATED")
   
    name = ""
    start_time = time.time()    
    actual_second = 0

    while True: 
  
        # print("In thraed " + str(threadnumber) + " @ " + str(msg_sent_counter) + " sent messages and " + str(msg_recv_counter) + " recieved")

        # print("server ", len(name))

        # data received from client 
        try:
            data = recv_timeout(c, 1024, 10) 
            if not data: 
                print('Bye thread' + str(threadnumber)) 
                
                # lock released on exit 
                break
    
            # reverse the given string from client 
            data = data.decode("utf-8") 

            msg_recv_counter = msg_recv_counter + 1
            avg_msg_recv_counter = avg_msg_recv_counter + 1



            # print(str(data))

            temp = str(data).split("-")
            while "" in temp:
                temp.remove("")


               # for t in temp:
            if "motor" in temp[-1]:
                c.send(str(shared_data["motor"]).encode("utf-8")) 




            # for t in temp:
            if "dmx" in temp[-1]:
                c.send(to_string(shared_data["dmx"]).encode("utf-8")) 


            if "led" in temp[-1] and "2" not in temp[-1]  :
                c.send(to_string(shared_data["led_right"]).encode("utf-8")) 
        
            if "led2" in temp[-1]:
                c.send(to_string(shared_data["led_left"]).encode("utf-8")) 
        


            if "taster_left" in str(data) or "taster_right" in str(data):
                if "im fine" in temp[-1]:
                    pass
                else:
                    if "right" in str(data):
                        name = "right"
                    else:
                        name = "left"
       

                for t in temp:
                    t.replace("taster_" + name, "")
                    ## print(t)
                    if "A:" in t and "D:" in t:
                        activation = []
                        for d in t:
                            if d == "1" or d == "0" :
                                activation.append(int(d))
                        if len(activation) == 4:
                            shared_data["taster_activation_" + name] = activation

            msg_sent_counter = msg_sent_counter + 1
        except Exception as e:

            ex_type, ex_value, ex_traceback = sys.exc_info()
            print(ex_type) 
            print(ex_value) 
            print(ex_traceback)



            print('Bye thread ' + str(threadnumber) + "  whatchdog barks ") 
            break

        

    # connection closed 
    c.close() 
  
  
def Main(): 
    host = "0.0.0.0" 
    port = 8090

    while 1:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            s.bind((host, port)) 
            break
        except:
            print("Port is busy, try again..")
            time.sleep(1)
          
  
    print("socket binded to port", port) 
  
    # put the socket into listening mode 
    s.listen(5) 
    print("socket is listening") 
    threadnumber = 0
    clients = []
    whatchdog = 0

   


    shared_data = {'dmx' : [0] * 512}
    shared_data['led_left'] = np.array([255] * 450)
    shared_data['led_right'] = np.array([255] * 450)
    shared_data["motor"] = 0

    shared_data["taster_activation_left"] = [0] * 4
    shared_data["taster_activation_right"] = [0] * 4




    ## audio player object
    shared_data["ap"] = AudioPlayer()


    # #################################################################################
    # #################################################################################
    # #################################################################################
    # #################################################################################
    # LC or automated DESIGN ##########################################################
    # true for digital light console
    if False:
        ## Start GUI
        gui_thread = threading.Thread(target=thread_function_gui, args=(shared_data, ))
        gui_thread.start()
    else:
        design_thread = threading.Thread(target=thread_function_design, args=(shared_data, ))
        design_thread.start()
    # #################################################################################
    # #################################################################################



    
   

    # a forever loop until client wants to exit 
    while True: 
        whatchdog += 1
        if whatchdog > 10:
            return
        # establish connection with client
        timeout = s.gettimeout()
        s.settimeout(1)

        s.listen(5)
        try:
            c, addr = s.accept() 
            print('Server accepted client') 

            # lock acquired by client 
            print('Connected to :', addr[0], ':', addr[1]) 
    
            # Start a new thread and return its identifier 
            sv_socket = threading.Thread(target=thread_function_sockets, args=([c, threadnumber, shared_data], ))
            clients.append(sv_socket)
            sv_socket.start()


            threadnumber = threadnumber +1
        except:
            e = sys.exc_info()[0]  
            # print("Server: no new clients", whatchdog)



def recv_timeout(sock, bytes_to_read, timeout_seconds):
    sock.setblocking(0)
    ready = select.select([sock], [], [], timeout_seconds)
    if ready[0]:
        return sock.recv(bytes_to_read)

    raise socket.timeout()


    
def to_string(list):
    out = ""
    for l in list:
        out += str(l) + ","
    return out


if __name__ == '__main__': 
    Main() 

