import socket
import sys
import codecs
import binascii
import struct
import time, datetime
import cmdframe
import PMUinfo
import array

def pmu(datA):
    # print(len(datA))
    # print(f"Received {datA!r}")
    POSIX=int.from_bytes(datA[6:10], "big")
    FRACSEC=int.from_bytes(datA[10:14], "big")
    SOC=POSIX+FRACSEC/1e6
    timestamp = datetime.datetime.fromtimestamp(SOC)
    # print(timestamp)
    STAT="{:064b}".format(int.from_bytes(datA[14:16], "big"))
    # print(STAT)
    Phasor=[]
    for i in range(16,64,4):
        phasor=struct.unpack('>f', datA[i:i+4]) 
        # CHNAM=CHNAM.rstrip('\x00')
        Phasor.append(phasor)
    # Phasor= struct.unpack('>f', datA[16:20]) 
    # Phasor=int.from_bytes(datA[16:18], "big")
    # print(Phasor)
    freq=struct.unpack('>f', datA[64:68]) 
    # print(freq)
    dfreq=struct.unpack('>f', datA[68:72]) 
    # print(dfreq)
    Analog=[]
    for i in range(72,124,4):
        analog=struct.unpack('>f', datA[i:i+4]) 
        # CHNAM=CHNAM.rstrip('\x00')
        Analog.append(analog)
    # print(Analog)
    Digital="{:064b}".format(int.from_bytes(datA[124:132], "big"))
    # print(Digital)
    pmudata=(timestamp, STAT, Phasor, freq, dfreq, Analog, Digital)
    return pmudata