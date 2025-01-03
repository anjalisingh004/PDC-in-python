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

HOST = ["172.26.82.225","172.24.134.6"] # The server's hostname or IP address
PORT = [10943,4713]  # The port used by the server
IDs=[43,2]

for host, port, ID in zip(HOST, PORT, IDs):
    ADDR = (host, port)
    
    # Connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    cmd=1
    CMDm=cmdframe.cfg(cmd,ID)
    #print(CMDm)
    #client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client.connect(ADDR)
    client.send(CMDm)
    CFGF = client.recv(2000)
    #print (CFGF)
    INFO=PMUinfo.pmuinfo(CFGF)
    print(f"Received {INFO!r}")
client.close()
