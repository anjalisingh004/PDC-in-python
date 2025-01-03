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

HOST = ["172.26.82.225", "172.24.134.6"]
PORT = [10943, 4713]
ID = [43, 2]

for host, port, pmu_id in zip(HOST, PORT, ID):
    ADDR = (host, port)
    
    # Connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)


# Connect to the server (establish connection outside the loop)
#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect((HOST, PORT))

# Initial commands (can be done outside the loop if needed)
cmd = 5
CMDm = cmdframe.cfg(cmd, pmu_id)
client.send(CMDm)
CFGF = client.recv(2000)
INFO = PMUinfo.pmuinfo(CFGF)
print(f"Received {INFO!r}")

cmd = 2
CMDm = cmdframe.cfg(cmd, pmu_id)
client.send(CMDm)
CFGF = client.recv(2000)
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
