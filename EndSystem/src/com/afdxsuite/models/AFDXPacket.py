from com.afdxsuite.core.network.scapy import Ether, Padding, Raw
from com.afdxsuite.config import Factory
from com.afdxsuite.logging import afdxLogger

class AFDXPacket(object):
    __packet = None
    conf_vl = None

    def __init__(self, packet):
        self.__packet = packet
        self.conf_vl = Factory.GET_InputVl(self.getDestinedVl())

    def getDestinedVl(self):
        dst_mac = self.__packet[Ether].dst
        vl_id = (str(dst_mac)[-5:]).replace(':', '')
        return int(vl_id, 16)

    def getFrameSequenceNumber(self):
        padding = self.__packet[Padding]
        if padding != None:
            load = padding.load
            return ord(load[-1])
        else:
            afdxLogger.error("Packet has no sequence number. Not an AFDX packet")

    def getPayload(self):
        payload = self.__packet[Raw].load
        return payload

    def getRawPacket(self):
        return self.__packet

    def __getitem__(self, item):
        return self.__packet[item]
