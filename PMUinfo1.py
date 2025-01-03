def PMUinfo(CFG1):
    sync_byte = int.from_bytes(CFG1[0:1], byteorder='big')
    C = {'sync_byte': sync_byte}

    type_byte = format(CFG1[1], '08b')
    type_byte = [int(bit) for bit in type_byte]

    frame_type = ''
    if int(''.join(map(str, type_byte[4:7])), 2) == 0:
        frame_type = 'DATA Frame'
    elif int(''.join(map(str, type_byte[4:8])), 2) == 1:
        frame_type = 'Header frame'
    elif int(''.join(map(str, type_byte[4:8])), 2) == 2:
        frame_type = ' Configuration Frame 1'
    elif int(''.join(map(str, type_byte[4:8])), 2) == 3:
        frame_type = ' Configuration Frame 2'
    elif int(''.join(map(str, type_byte[4:8])), 2) == 4:
        frame_type = ' Configuration Frame 3'
    elif int(''.join(map(str, type_byte[4:8])), 2) == 5:
        frame_type = 'Command Frame (received message)'
    C['frame_type'] = frame_type
    
##    if int(''.join(map(str, type_byte[0:4])), 2) == 1:
##        frame_version = 'Version 1:IEEE Std C37.118-2005 [B6]'
##    elif int(''.join(map(str, type_byte[0:4])), 2) == 2:
##        frame_version = 'Version 2:IEEE Std C37.118.2-2011'
##    C['frame_version'] = frame_version


    frame_length = int.from_bytes(CFG1[2:4], byteorder='big')
    C['frame_length'] = frame_length

    ID_code = int.from_bytes(CFG1[4:6], byteorder='big')
    C['ID_code'] = ID_code

    soc = int.from_bytes(CFG1[6:10], byteorder='big')
    C['soc'] = soc

    fracsec = int.from_bytes(CFG1[10:14], byteorder='big')
    C['fracsec'] = fracsec

    time_base = int.from_bytes(CFG1[14:18], byteorder='big')
    C['time_base'] = time_base

    NUM_PMU = int.from_bytes(CFG1[18:20], byteorder='big')
    C['NUM_PMU'] = NUM_PMU

    STN = CFG1[20:36].decode('utf-8').rstrip('\x00')
    C['STN'] = STN

    source_id = int.from_bytes(CFG1[36:38], byteorder='big')
    C['source_id'] = source_id

    format_byte = format(CFG1[39], '08b')
    #format_byte = [int(bit) for bit in format_byte]
    format_byte = [int(bit) for bit in format_byte[::-1]]
    if format_byte[0] == 1:
        Phasor_coordinate_format = 'Polar'
    elif format_byte[0] == 0:
        Phasor_coordinate_format = 'Rectangular'
    C['Phasor_coordinate_format'] = Phasor_coordinate_format

    if format_byte[1] == 1:
        Phasor_data_format = 'Floating point'
    elif format_byte[1] == 0:
        Phasor_data_format = '16 bit Integer'
    C['Phasor_data_format'] = Phasor_data_format

    if format_byte[2] == 1:
        Analog_data_format = 'Floating Point'
    elif format_byte[2] == 0:
        Analog_data_format = '16 bit Integer'
    C['Analog_data_format'] = Analog_data_format

    if format_byte[3] == 1:
        Frequency_data_format = 'Floating Point'
    elif format_byte[3] == 0:
        Frequency_data_format = '16 bit Integer'
    C['Frequency_data_format'] = Frequency_data_format

    PHNMR = int.from_bytes(CFG1[40:42], byteorder='big')
    ANNMR = int.from_bytes(CFG1[42:44], byteorder='big')
    DGNMR = int.from_bytes(CFG1[44:46], byteorder='big')
    C['PHNMR'] = PHNMR
    C['ANNMR'] = ANNMR
    C['DGNMR'] = DGNMR

    j = 20 + 27
    phasor = CFG1[j:j + PHNMR * 16]
    PhasorN = phasor.decode('utf-8').rstrip('\x00')
    C['PhasorN'] = PhasorN

    j = 20 + 26 + PHNMR * 16 + 1
    analog = CFG1[j:j + ANNMR * 16]
    AnalogN = analog.decode('utf-8').rstrip('\x00')
    C['AnalogN'] = AnalogN

##    j = 20 + 26 + PHNMR * 16 + ANNMR * 16 + 1
##    digital = CFG1[j:j + DGNMR * 16 * 16]
##    DigitalN = digital.decode('utf-8').rstrip('\x00')
##    C['DigitalN'] = DigitalN

    DIGITAL_OFFSET = 20 + 26 + PHNMR * 16 + ANNMR * 16
    DIGITAL_LENGTH = 16

    CHNAM1 = []
    for i in range(DIGITAL_OFFSET, DIGITAL_OFFSET + DGNMR * DIGITAL_LENGTH * 16, DIGITAL_LENGTH):
        CHNAM = CFG1[i:i + DIGITAL_LENGTH].decode('utf-8').rstrip('\x00')
        CHNAM1.append(CHNAM)

        C['DigitalN'] = CHNAM1


    j = 16 * DGNMR * 16 + (16 * ANNMR + (PHNMR * 16 + 20 + 26))
    PHUNIT = CFG1[j:j + 4 * PHNMR]

    phasor_type = []
    phasor_scale = []

    for i in range(0, len(PHUNIT), 4):
        PP = PHUNIT[i:i+4]
        x = int(PP[0])  # MSB for phasor type
        y = int(PP[-1])  # LSB for phasor scale
        phasor_type.extend(['voltage' if x == 0 else 'current' if x == 1 else 'unknown'])
        phasor_scale.extend([y])

    C['phasor_type'] = phasor_type
    C['phasor_scale'] = phasor_scale

   


    j = 16 * DGNMR * 16 + (16 * ANNMR + (PHNMR * 16 + 20 + 26)) + 4 * PHNMR 
    ANUNIT = CFG1[j:j + 4 * ANNMR]

    analog_type = []

    for i in range(0, len(ANUNIT), 4):
        AA = ANUNIT[i:i + 4]  # Extract four bytes starting from index i
        x = int(AA[0])
        analog_type.append('single Point on Waveform' if x == 0 else 'RMS' if x == 1 else 'Peak Value' if x == 2 else str(x))

    C['analog_type'] = analog_type

    

    j = 16 * DGNMR * 16 + (16 * ANNMR + (PHNMR * 16 + 20 + 26)) + 4 * PHNMR + 4 * ANNMR + 1
    DGUNIT = CFG1[j:j + 4 * DGNMR]

    FNOM = int.from_bytes(CFG1[16 * DGNMR * 16 + (16 * ANNMR + (PHNMR * 16 + 20 + 26)) + 4 * PHNMR + 4 * ANNMR + 4 * DGNMR + 1:16 * DGNMR * 16 + (16 * ANNMR + (PHNMR * 16 + 20 + 26)) + 4 * PHNMR + 4 * ANNMR + 4 * DGNMR + 2], byteorder='big')
    Freq_nominal = 50 if FNOM == 1 else 60
    C['Freq_nominal'] = Freq_nominal

    Change_count = int.from_bytes(CFG1[16 * DGNMR * 16 + (16 * ANNMR + (PHNMR * 16 + 20 + 26)) + 4 * PHNMR + 4 * ANNMR + 4 * DGNMR + 2 + 1:16 * DGNMR * 16 + (16 * ANNMR + (PHNMR * 16 + 20 + 26)) + 4 * PHNMR + 4 * ANNMR + 4 * DGNMR + 2 + 2], byteorder='big')
    C['Change_count'] = Change_count

    data_rate = int.from_bytes(CFG1[16 * DGNMR * 16 + (16 * ANNMR + (PHNMR * 16 + 20 + 26)) + 4 * PHNMR + 4 * ANNMR + 4 * DGNMR + 1 + 2 + 2:16 * DGNMR * 16 + (16 * ANNMR + (PHNMR * 16 + 20 + 26)) + 4 * PHNMR + 4 * ANNMR + 4 * DGNMR + 1 + 2 + 2 + 1], byteorder='big')
    C['data_rate'] = data_rate

    return C

