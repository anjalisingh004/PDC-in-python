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

HOST = ["172.26.82.225", "172.24.134.6"]  # The server's hostname or IP address
PORT = [10943, 4713]  # The port used by the server
IDs = [43, 2]



# Create a list to store socket connections
clients = []

# Connect to each PMU
for host, port in zip(HOST, PORT):
    ADDR = (host, port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    clients.append(client)

try:
    # Continuous data reading loop
    while True:
        for client, ID in zip(clients, IDs):
            # Send command to PMU
            cmd = 5
            CMDm = cmdframe.cfg(cmd, ID)
            client.send(CMDm)
            CMDm = cmdframe.cfg(cmd, ID)
            client.send(CMDm)
            cmd = 1
            CMDm = cmdframe.cfg(cmd, ID)
            client.send(CMDm)
            CMDm = cmdframe.cfg(cmd, ID)
            client.send(CMDm)
            CFGF = client.recv(2000)
            INFO = PMUinfo.pmuinfo(CFGF)
            print(f"Received {INFO!r}")
            
            # Receive data from PMU
            datA = client.recv(2000)
            pmudata = PMU.pmu(datA)
            print(f"Received data from PMU {ID}: {pmudata}")
finally:
    # Close connections when done
    for client in clients:
        client.close()
##def receive_data(client):
##    while True:
##        datA = client.recv(2000)
##        # Do whatever processing you need with the received data
##        pmudata = PMU.pmu(datA)
##        print(pmudata)

def main():
    threads = []
    for host, port, ID in zip(HOST, PORT, IDs):
        ADDR = (host, port)

        # Connect to the server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        cmd = 2
        CMDm = cmdframe.cfg(cmd, ID)
        client.send(CMDm)
        CFGF = client.recv(2000)
        INFO = PMUinfo.pmuinfo(CFGF)
        print(f"Received {INFO!r}")
        cmd = 2
        CMDm = cmdframe.cfg(cmd, ID)
        client.send(CMDm)

        thread = threading.Thread(target=receive_data, args=(client,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
