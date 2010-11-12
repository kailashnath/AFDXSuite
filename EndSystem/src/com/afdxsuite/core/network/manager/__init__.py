
SEQUENCE_FRAME = 0
SEQUENCE_VL = 1

PRSN = {}
PASN = {}

def reset():
    global PRSN, PASN
    PRSN = {}
    PASN = {}

def getPRSN(vlId):
    global PRSN
    
    if vlId != None and PRSN.has_key(vlId):
        return PRSN[vlId]
    else:
        return -1

def setRSN(vlId, sn):
    global PRSN

    if vlId != None and sn != None:
        PRSN[vlId] = sn

def getPASN(vlId):
    global PASN
    
    if vlId != None and PASN.has_key(vlId):
        return PASN[vlId]
    else:
        return -1

def setASN(vlId, sn):
    global PASN
    
    if vlId != None and sn != None:
        PASN[vlId] = sn

def getNextSequenceNumber(sn, type):
    if type == SEQUENCE_FRAME:
        if sn == 255:
            return 1
        else:
            return sn + 1
    elif type == SEQUENCE_VL:
        if sn == 65535:
            return 1
        else:
            return sn + 1
