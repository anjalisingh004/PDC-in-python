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

HOST = "172.26.82.225"
PORT = 10943
ID = 43



# Connect to the server (establish connection outside the loop)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Initial commands (can be done outside the loop if needed)


cmd = 1
CMDm = cmdframe.cfg(cmd, ID)
client.send(CMDm)
#CFGF = client.recv(2000)
# INFO = PMUinfo.pmuinfo(CFGF)
# print(f"Received {INFO!r}")
 
buffer = ''
while True:
    # Receive data in chunks
    data = client.recv(2000)  # Adjust buffer size as needed

    # Check for empty data (client disconnected)
    # if not data:
    #    break

    # Process received data (append or handle complete data)
    
    pmudata = PMU.pmu(data)  # Process data based on your PMU protocol
    print(pmudata)

    # Clear buffer if data processing is complete (optional)
    buffer = ''  # Reset buffer if processing doesn't require accumulating data

# Close the socket after exiting the loop
client.close()
