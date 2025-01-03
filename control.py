import socket
import sys
import cmdframe
import send 

HOST = "172.26.82.225"
PORT = 10943
ADDR = (HOST, PORT)
ID = 43

def control_data(cmd):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    # Generate configuration command based on the provided command (1 for turn off, 2 for turn on)
    CMDm = cmdframe.cfg(cmd, ID)
    client.send(CMDm)

    client.close()

if __name__ == "__main__":
    cmd = int(input("Enter command (1 for turn off, 2 for turn on): "))
    control_data(cmd)
