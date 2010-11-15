from com.afdxsuite.core.network.manager import SEQUENCE_FRAME, SEQUENCE_VL,\
    SEQUENCE_IP

class SequenceHandler(object):

    def __init__(self):
        self.PRSN = {}
        self.PASN = {}

        # RFSN : Running frame sequence number
        self.RFSN = {}
        
        self.__current_ip_id = 30

    def getPRSN(self, vlId):

        if vlId != None and self.PRSN.has_key(vlId):
            return self.PRSN[vlId]
        else:
            return -1

    def setRSN(self, vlId, sn):
        if vlId != None and sn != None:
            self.PRSN[vlId] = sn
    
    def getPASN(self, vlId):
        if vlId != None and self.PASN.has_key(vlId):
            return self.PASN[vlId]
        else:
            return -1

    def setASN(self, vlId, sn):
        if vlId != None and sn != None:
            self.PASN[vlId] = sn
    
    def getNextSequenceNumber(self, sn, type):
        if type == SEQUENCE_FRAME:
            if sn == 255:
                return 1
            else:
                return sn + 1
        elif type == SEQUENCE_VL or type == SEQUENCE_IP:
            if sn == 65535:
                return 1
            else:
                return sn + 1

    def getNextFrameSequenceNumber(self, vlId):
        sn = 0
        if self.RFSN.has_key(vlId):
            sn = self.RFSN[vlId]

        self.RFSN[vlId] = self.getNextSequenceNumber(sn, SEQUENCE_IP)
        return sn

    def getNextIpId(self):
        self.__current_ip_id = self.getNextSequenceNumber(self.__current_ip_id,
                                                          type)
        return self.__current_ip_id

    def reset(self, vlId = None):
        if vlId == None:
            self.PASN.clear()
            self.PRSN.clear()
            self.RFSN.clear()
        else:
            if self.PASN.has_key(vlId):
                self.PASN[vlId] = -1
            if self.PRSN.has_key(vlId):
                self.PRSN[vlId] = -1

        print "Sequence handler is reset"
