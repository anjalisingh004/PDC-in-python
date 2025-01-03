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
import asyncio

HOST = "172.26.82.225"  # The server's hostname or IP address
PORT = 10943  # The port used by the server
ADDR = (HOST, PORT)
ID = 43




async def process_data(client):
    loop = asyncio.get_event_loop()
    while True:
        data = await loop.sock_recv(client, 2000)
        if not data:
            break
        pmudata = PMU.pmu(data)
        print(pmudata)
        await asyncio.sleep(0)  # Allow other tasks to run


async def main():
    while True:
        command = input("Enter command : ").strip().lower()
        if command not in ["1", "2"]:
            print("Invalid command. Please enter 'on' or 'off'.")
            continue

        if command == "2":
            # Connect to the server
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
            CMDm = cmdframe.cfg(2, ID)

            print("Sending command:", CMDm)
            client.send(CMDm)
            

            # Start processing data asynchronously
            await process_data(client)
            
            
        elif command == "1":
            print("Data processing is OFF")
            # Put any code here for when data processing is OFF
            # For example, you may choose to pause or exit the script
            await asyncio.sleep(1)  # Sleep to avoid CPU hogging


if __name__ == "__main__":
 asyncio.run(main())
