
# import socket programming library 
import socket 
  
import math
import sys  
# import thread module 
import threading 
import select
from GUI import GUI

print_lock = threading.Lock() 
  
import time  
# thread function 


def recv_timeout(sock, bytes_to_read, timeout_seconds):
    sock.setblocking(0)
    ready = select.select([sock], [], [], timeout_seconds)
    if ready[0]:
        return sock.recv(bytes_to_read)

    raise socket.timeout()


def thread_function_gui(shared_information):
    print("thead startest für hui")
    print(shared_information)
    gui = GUI(shared_information)
    



def thread_function_sockets(data):
    c = data[0]
    avg_msg_recv_counter = 0
    msg_sent_counter = 0
    msg_recv_counter = 0
    threadnumber = data[1] 
    shared_information = data[2]

    print("******************************************")
    print("THREAD " + str(threadnumber) + " INITIATED")
   
    name = ""
    start_time = time.time()    
    actual_second = 0

    while True: 
  
        print("In thraed " + str(threadnumber) + " @ " + str(msg_sent_counter) + " sent messages and " + str(msg_recv_counter) + " recieved")

        print("server ", len(name))


        # data received from client 
        try:
            data = recv_timeout(c, 1024, 3) 
            if not data: 
                print('Bye thread' + str(threadnumber)) 
                
                # lock released on exit 
                break
    
            # reverse the given string from client 
            data = data.decode("utf-8") 

            msg_recv_counter = msg_recv_counter + 1
            avg_msg_recv_counter = avg_msg_recv_counter + 1


            if "name:" in str(data):
                name = data.split("name:")[1].split("-")[0]
                print(data.split("name:"))
                print(data.split("name:")[1])
                if len(name) == 0:
                    print(name + " error error")
                shared_information["client_state_" + name] = 1
                shared_information["client_activation_" + name] = [0] * 8
                shared_information["client_led_" + name] = False
                shared_information["client_msg_" + name] = ""
                shared_information["client_msgs_" + name] = 0


            print(str(data))

            temp = str(data).split("-")
            while "" in temp:
                temp.remove("")
            print(temp)

            for t in temp:

                if "A:" in t:
                    activation = []
                    for d in t:
                        if d == "1" or d == "0" :
                            activation.append(int(d))
                    if len(activation) == 8:
                        shared_information["client_activation_" + name] = activation

    
            # send back reversed string to client 
            

            if shared_information["client_led_" + name]:

                c.send("LEDON super gemacht".encode("utf-8")) 
            else:
                c.send("LEDOFF super gemacht".encode("utf-8")) 


            second = math.floor(time.time() - start_time)
            if actual_second != second:
                avg_msg_recv_counter = 0
                actual_second = second
            else:
                temp = str(1 / ((time.time() - start_time) % 1) * avg_msg_recv_counter)


                if len(temp) > 5:
                    shared_information["client_msgs_" + name] = temp[0:6]
                else:
                    shared_information["client_msgs_" + name] = temp




            shared_information["client_msg_" + name] =  str(data) + " @ " + str((time.time() - start_time))

            msg_sent_counter = msg_sent_counter + 1
        except Exception as e:

            ex_type, ex_value, ex_traceback = sys.exc_info()
            print(ex_type) 
            print(ex_value) 
            print(ex_traceback)

            shared_information["client_state_" + name] = 0
            shared_information["client_msgs_" + name] = 0

            print('Bye thread' + str(threadnumber) + "  whatchdog barks ") 
            break

        

    # connection closed 
    c.close() 
  
  
def Main(): 
    host = "0.0.0.0" 
    port = 8090

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    print("socket binded to port", port) 
  
    # put the socket into listening mode 
    s.listen(5) 
    print("socket is listening") 
    threadnumber = 0
    clients = []
    whatchdog = 0


    shared_information = {'msg_gui_to_ss': [] , 'msg_ss_to_gui': []}


    ## Start GUI
    gui_thread = threading.Thread(target=thread_function_gui, args=(shared_information, ))
    gui_thread.start()



    # a forever loop until client wants to exit 
    while True: 

        whatchdog += 1
        if whatchdog > 99999:
            return
        # establish connection with client
        timeout = s.gettimeout()
        s.settimeout(1)

        print(timeout)
        s.listen(5)
        try:
            c, addr = s.accept() 
            print('Server accepted client') 

            # lock acquired by client 
            print('Connected to :', addr[0], ':', addr[1]) 
    
            # Start a new thread and return its identifier 
            sv_socket = threading.Thread(target=thread_function_sockets, args=([c, threadnumber, shared_information], ))
            clients.append(sv_socket)
            sv_socket.start()


            threadnumber = threadnumber +1
        except:
            e = sys.exc_info()[0]  
            print("Server: no new clients", whatchdog)

if __name__ == '__main__': 
    Main() 
