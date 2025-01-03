import socket
import sys
import codecs
import binascii
import struct
import time, datetime
import cmdframe
import PMUinfo1
import array
import PMU

HOST = ["172.26.82.225","172.24.134.6"] # The server's hostname or IP address
PORT = [10943,4713]  # The port used by the server
IDs=[43,2]
received_data={}
PMU_cfg = {} 
for host, port, ID in zip(HOST, PORT, IDs):
    ADDR = (host, port)
    # Connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(client)
    cmd=5
    CMDm=cmdframe.cfg(cmd,ID)
    client.send(CMDm)
    CFGF = client.recv(2000)
    
    INFO=PMUinfo1.PMUinfo(CFGF)
    # Store PMU_cfg in the dictionary with ID as the key
    PMU_cfg[ID] = INFO
    # print PMU_cfg[2] and PMU_cfg[43] in entering these variables in output window
##    print(f"Received {INFO!r}")
while True:
    cmd=2
    CMDm=cmdframe.cfg(cmd,ID)
    client.send(CMDm)
    datA = client.recv(2000)
    # Do whatever processing you need with the received data
    pmudata = PMU.pmu(datA)
    received_data[ID] = pmudata
    print(received_data[ID])
##    print(pmudata)

##
##
### for i in range(n):
###def recieve_data():
##buffer = ''
##cmd = 2
##CMDm = cmdframe.cfg(cmd, ID)
##
##client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##client.connect(ADDR)
##        # Encoding data before sending
##client.send(CMDm)
##
##
##while True:
##    datA = client.recv(2000)
##    print(datA)
##    # Do whatever processing you need with the received data
##    pmudata = PMU.pmu(datA)
##    print(pmudata)



          





