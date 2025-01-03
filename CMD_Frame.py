
import sys
import codecs
import binascii
import struct
import time, datetime
import crc16
def cfg():
    d = datetime.datetime.now()
    SOC=time.mktime(d.timetuple())
    SOCb="{:032b}".format(int(SOC))
    SOCh=["{0:0>2X}".format(int(SOCb[:8], 2)), "{0:0>2X}".format(int(SOCb[8:16], 2)),
          "{0:0>2X}".format(int(SOCb[16:24], 2)),
          "{0:0>2X}".format(int(SOCb[24:32], 2))]
    #print(SOCh)
    FRACSEC=5600000
    FRACSECb="{:032b}".format(int(FRACSEC))
    FRACSECh=["{0:0>2X}".format(int(FRACSECb[:8], 2)), "{0:0>2X}".format(int(FRACSECb[8:16], 2)),
          "{0:0>2X}".format(int(FRACSECb[16:24], 2)),
          "{0:0>2X}".format(int(FRACSECb[24:32], 2))]
    #print(FRACSECh)
    CMDh=["{0:0>2X}".format(int(bin(0), 2)), "{0:0>2X}".format(int(bin(5), 2))]
    #print(CMDh)
    dat=datetime.datetime.utcnow().strftime("'%Y-%m-%d %H:%M:%S.%f'")[:-4]
    ID_CODE=4
    IDh=["{0:0>2X}".format(int(bin(0), 2)), "{0:0>2X}".format(int(bin(4), 2))]
    #print(IDh)
    SYNCh=["{0:0>2X}".format(int(bin(170), 2)), "{0:0>2X}".format(int(bin(65), 2))]
    #print(SYNCh)
    FRAMESIZEh=["{0:0>2X}".format(int(bin(0), 2)), "{0:0>2X}".format(int(bin(18), 2))]
    #print(FRAMESIZEh)
    cmdframe=SYNCh+FRAMESIZEh+IDh+SOCh+FRACSECh+CMDh
    #print(cmdframe)

    def listToString(s): 
        
        # initialize an empty string
        str1 = "" 
        
        # traverse in the string  
        for ele in s: 
            str1 += ele  
        
        # return string  
        return str1
    s = cmdframe
    s1=listToString(s)
    #print(listToString(s)) 
    hexadecimal_string = s1
    cmdframeB = bytearray.fromhex(hexadecimal_string)
    #print(cmdframeB)  


    '''   
    def crc16(data : bytearray, offset , length):
        if data is None or offset < 0 or offset > len(data)- 1 and offset+length > len(data):
            return 0
        crc = 0xFFFF
        for i in range(0, length):
            crc ^= data[offset + i] << 8
            for j in range(0,8):
                if (crc & 0x8000) > 0:
                    crc =(crc << 1) ^ 0x1021
                else:
                    crc = crc << 1
        return crc & 0xFFFF
    '''

    
    CRC=crc16.crc16(cmdframeB,0,len(cmdframeB))
    CRCb="{:016b}".format(CRC)
    CRCh=["{0:0>2X}".format(int(CRCb[:8], 2)), "{0:0>2X}".format(int(CRCb[8:16], 2))]
    #print(f"the CRC16 is{CRCh!r}")

    CMDFRAME = cmdframe+CRCh
    #print(CMDFRAME)
    s2 = CMDFRAME
    s3=listToString(s2)
    #print(listToString(s2)) 
    hexadecimal_string1 = s3
    CMDm = bytearray.fromhex(hexadecimal_string1)
    print(f"the output Dframe in bytearray is {CMDm!r}")
    #print(len(CMDm))
    return CMDm
