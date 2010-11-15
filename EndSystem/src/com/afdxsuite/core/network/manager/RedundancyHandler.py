from com.afdxsuite.core.network.manager import SEQUENCE_FRAME
from com.afdxsuite.core.network.manager.SequenceHandler import SequenceHandler

import threading
from com.afdxsuite.core.network.scapy import IP

class RedundancyHandler(object):

    __result = False
    __sequence_handler = None
    _accepted_sns = dict()

    def __init__(self):
        self.__sequence_handler = SequenceHandler()

    def __addAcceptedSN(self, vlId, sn):

        if self._accepted_sns.has_key(vlId):
            if len(self._accepted_sns[vlId]) > 10:
                self._accepted_sns[vlId] = self._accepted_sns[vlId][5:]
            self._accepted_sns[vlId].append(sn)
        else:
            self._accepted_sns[vlId] = [sn]

    def __getLatestAcceptedSNs(self, vlId):

        if self._accepted_sns.has_key(vlId):
            sns = self._accepted_sns[vlId]
            return sns[-5:]
        return tuple()

    def __checkForRedundancy(self, afdxPacket):
        rsn = afdxPacket.getFrameSequenceNumber()
        if rsn == None:
            return False
        vlId  = afdxPacket.getDestinedVl()
        pasn  = self.__sequence_handler.getPASN(vlId)
        
        # the below condition is as per the specification
        #acceptable_asn = [self.__sequence_handler.getNextSequenceNumber(
        #                                           pasn + i, SEQUENCE_FRAME) \
        #                 for i in range(0, 66)]

        # this condition is as per what kailash has thought of.
        # the dict "_accepted_sns" contains list of 5 recently accepted
        # sequence numbers for a vl. If the rsn is in any of the received
        # sn's then the packet is a redundant packet, hence reject else
        # accept and proceed forward
        acceptable_asn = self.__getLatestAcceptedSNs(vlId)
        #print pasn, rsn, acceptable_asn, vlId, rsn in acceptable_asn
        if (pasn == -1) or (rsn not in acceptable_asn):
            #print 'accepted'
            self.__sequence_handler.setASN(vlId, rsn)
            self.__addAcceptedSN(vlId, rsn)
            return True

        return False

    def doCheck(self, afdxPacket):
        self.__result = False

        if not self.__checkForRedundancy(afdxPacket):
            print 'Redundancy check failed for packet with ip id', \
            afdxPacket[IP].id
            #afdxLogger.error("The packet failed with redundancy check")
            return

        self.__result = True
        #afdxLogger.info("The packet has passed the redundancy check")

    def getResult(self):
        return self.__result

    def reset(self):
        self.__sequence_handler = SequenceHandler()
        self._accepted_sns.clear()
        self.__result = False
