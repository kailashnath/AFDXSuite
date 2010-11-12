from com.afdxsuite.logging import afdxLogger
from com.afdxsuite.core.network.manager import getPRSN, setRSN,\
    getNextSequenceNumber, SEQUENCE_FRAME

class IntegrityHandler(object):
    __result = False

    def __init__(self):
        pass

    def __doIntegrityCheck(self, afdxPacket):

        rsn = afdxPacket.getFrameSequenceNumber()
        if rsn == None:
            return False

        vl  = afdxPacket.getDestinedVl()
        prsn = getPRSN(vl)
        prsn_next_1 = getNextSequenceNumber(prsn, SEQUENCE_FRAME)
        prsn_next_2 = getNextSequenceNumber(prsn_next_1, SEQUENCE_FRAME)

        if (rsn in (prsn_next_1, prsn_next_2)) or \
            (rsn == 0 and prsn != 0) or \
            (prsn == -1):
            setRSN(vl, rsn)
            return True

    def doCheck(self, afdxPacket):
        self.__result = False

        if not self.__doIntegrityCheck(afdxPacket):
            afdxLogger.error("The packet failed integrity check")
            return

        self.__result = True
        #afdxLogger.info("The packet has passed the integrity check")

    def getResult(self):
        return self.__result
