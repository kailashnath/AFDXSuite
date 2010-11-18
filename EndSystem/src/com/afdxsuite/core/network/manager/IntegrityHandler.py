from com.afdxsuite.logging import afdxLogger
from com.afdxsuite.core.network.manager import SEQUENCE_FRAME
from com.afdxsuite.core.network.manager.SequenceHandler import SequenceHandler
from com.afdxsuite.core.network.scapy import IP, wireshark, Ether

class IntegrityHandler(object):
    __result = False
    __sequence_handler = None
    
    def __init__(self):
        self.__sequence_handler = SequenceHandler()

    def __isIntegrityValid(self, afdxPacket):

        rsn = afdxPacket.getFrameSequenceNumber()
        if rsn == None:
            return False

        vlId  = afdxPacket.getDestinedVl()
        prsn = self.__sequence_handler.getPRSN(vlId)
        prsn_next_1 = self.__sequence_handler.getNextSequenceNumber(prsn,
                                                                 SEQUENCE_FRAME)
        prsn_next_2 = self.__sequence_handler.getNextSequenceNumber(prsn_next_1,
                                                                 SEQUENCE_FRAME)

        if (rsn in (prsn_next_1, prsn_next_2)) or (prsn == -1) or \
        (rsn == 0 and prsn != 0):
            if (rsn == 0 and prsn != 0):
                self.__sequence_handler.setASN(vlId, 0)
            self.__sequence_handler.setRSN(vlId, rsn)
            return True
        return False

    def doCheck(self, afdxPacket):
        self.__result = False

        if not self.__isIntegrityValid(afdxPacket):
            if afdxPacket[IP] != None:
                print "Integrity check failed for packet with ip id", \
                        afdxPacket[IP].id
            #afdxLogger.error("The packet failed integrity check")
            return

        self.__result = True
        #afdxLogger.info("The packet has passed the integrity check")

    def getResult(self):
        return self.__result

    def reset(self):
        self.__sequence_handler = SequenceHandler()
