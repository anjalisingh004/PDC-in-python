def pmuinfo(CFGF):
    CFGFs = bytes(CFGF)
    PHNMR=int.from_bytes(CFGF[41:42], "big")
    ANNMR=int.from_bytes(CFGF[43:44], "big")
    DGNMR=int.from_bytes(CFGF[45:46], "big")
    #print(PHNMR)
    #print(ANNMR)
    #print(DGNMR)
    # Channel Names decoded here
    CHNAM1=[]
    for i in range(46,16*(PHNMR+ANNMR+16*DGNMR)+32,16):
        CHNAM=CFGF[i:i+15].decode();
        CHNAM=CHNAM.rstrip('\x00')
        CHNAM1.append(CHNAM)

    #print(CFGF[i:i+15].decode())
    #print(CFGF[i:i+15].decode())
    #Format 16 bit flag word decoded here
        
    Format=int.from_bytes(CFGF[39:40], "big")
    FORMAT="{:016b}".format(Format)
    #print(FORMAT)
    ####PHUNIT/ANUNIT/DGUNIT decoded here
    for i in range(16*DGNMR*16+(16*ANNMR+(PHNMR*16+20+26))+1,16*DGNMR*16+(16*ANNMR+(PHNMR*16+20+26))+4*PHNMR+4*ANNMR+4*DGNMR,4):

            UNIT="{:032b}".format(int.from_bytes(CFGF[i:i+3], "big"));
            #print("{:032b}".format(int.from_bytes(CFGF[i:i+3], "big")))
    ## Nimonal frequency
    F=int.from_bytes(CFGF[(16*DGNMR*16+(16*ANNMR+(PHNMR*16+20+26))+4*PHNMR+4*ANNMR+4*DGNMR+1):
                                (16*DGNMR*16+(16*ANNMR+(PHNMR*16+20+26))+4*PHNMR+4*ANNMR+4*DGNMR+2)], "big")
    if F==0:
        F_nominal=60
        #print("60Hz")
    else:
        F_nominal=50
        #print("Nimonal Frequency- 50hz")
    DATA_RATE=int.from_bytes(CFGF[(16*DGNMR*16+(16*ANNMR+(PHNMR*16+20+26))+4*PHNMR+4*ANNMR+4*DGNMR+1+2+2):
                             (16*DGNMR*16+(16*ANNMR+(PHNMR*16+20+26))+4*PHNMR+4*ANNMR+4*DGNMR+2+2+2)], "big")
    #print(f"Reporting Rate- {DATA_RATE!r}")
    CFGCNT=int.from_bytes(CFGF[(16*DGNMR*16+(16*ANNMR+(PHNMR*16+20+26))+4*PHNMR+4*ANNMR+4*DGNMR+3):
                             (16*DGNMR*16+(16*ANNMR+(PHNMR*16+20+26))+4*PHNMR+4*ANNMR+4*DGNMR+4)], "big")
    #print(f"configuration Change- {CFGCNT!r}")
 
    info=(PHNMR, ANNMR, DGNMR, CHNAM1, F_nominal, DATA_RATE, CFGCNT)
    return info