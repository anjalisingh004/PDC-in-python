import socket
import sys
import codecs
import binascii
import struct
import time, datetime
import cmdframe
import PMUinfo
import array
import PMU
import threading


HOST = "172.26.82.225"  # The server's hostname or IP address
PORT = 10943  # The port used by the server


ADDR=(HOST,PORT)
ID=43



'''HOST = "172.24.134.5"  # The server's hostname or IP address
#PORT = 4713  # The port used by the server
ID=2'''


cmd=5
CMDm=cmdframe.cfg(cmd,ID)
#print(CMDm)
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
client.send(CMDm)
CFGF = client.recv(2000)
#print (CFGF)
INFO=PMUinfo.pmuinfo(CFGF)
#print(f"Received {INFO!r}")

'''HOST = "172.24.134.5"  # The server's hostname or IP address
PORT = 4713  # The port used by the server
ID=2
cmd=2
CMDm=cmdframe.cfg(cmd,ID)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     s.connect((HOST, PORT))
     s.send(CMDm)
     CFGF = s.recv(2000)
INFO=PMUinfo.pmuinfo(CFGF)
print(f"Received {INFO!r}")'''









buffer = ''
cmd = 2
CMDm = cmdframe.cfg(cmd, ID)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
# Encoding data before sending
client.send(CMDm)
CMDm = cmdframe.cfg(cmd, ID)
client.send(CMDm)

def f1():
      while True:
        datA = client.recv(2000)
        # print(datA)
        # Do whatever processing you need with the received data
        pmudata = PMU.pmu(datA)
        # print(pmudata)









def f2():   
       while True:
         cmd = input("Enter cmd (1 to stop, any other cmd to continue): ")

    # Send the command based on user input
         if cmd == "1":
             stop_cmd = cmdframe.cfg(1, ID)
             print("Connection closed.")
             #break # Exit the loop to stop data reception
         else:
            try:
                cmd_int = int(cmd)
                CMDm = cmdframe.cfg(cmd_int, ID)
                print("Sending command:", CMDm)
                client.send(CMDm)

            except ValueError:
                print("Invalid input. Please enter a valid command.")

if __name__ == "__main__":
    thread1 = threading.Thread(target=f1)
    thread2 = threading.Thread(target=f2)

    
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


# Close the client socket
    client.close()