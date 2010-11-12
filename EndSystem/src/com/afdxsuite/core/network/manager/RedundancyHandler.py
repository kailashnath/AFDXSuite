from com.afdxsuite.logging import afdxLogger
from com.afdxsuite.core.network.manager import getNextSequenceNumber,\
    SEQUENCE_FRAME, getPASN, setASN

class RedundancyHandler(object):

    __result = False

    def __init__(self):
        pass

    def __checkForRedundancy(self, afdxPacket):
        rsn = afdxPacket.getFrameSequenceNumber()
        if rsn == None:
            return False
        vlId  = afdxPacket.getDestinedVl()
        pasn = getPASN(vlId)
        acceptable_asn = [getNextSequenceNumber(pasn + i, SEQUENCE_FRAME) \
                          for i in range(0, 66)]

        if (pasn == -1) or (rsn in acceptable_asn):
            setASN(vlId, rsn)
            return True

        return False

    def doCheck(self, afdxPacket):
        self.__result = False

        if not self.__checkForRedundancy(afdxPacket):
            afdxLogger.error("The packet failed with redundancy check")

        self.__result = True
        #afdxLogger.info("The packet has passed the redundancy check")

    def getResult(self):
        return self.__result
