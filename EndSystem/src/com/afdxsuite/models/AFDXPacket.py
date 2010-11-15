from com.afdxsuite.core.network.scapy import Ether, Padding, Raw, IP, UDP
from com.afdxsuite.logging import afdxLogger
from com.afdxsuite.config import Factory
from com.afdxsuite.core.network import NETWORK_A, NETWORK_AB

class AFDXPacket(object):
    __packet = None
    conf_vl = None

    def __init__(self, packet = None, port = None):
        if packet != None:
            self.__packet = packet
            if packet[UDP] == None:
                return
            self.conf_vl = Factory.GET_InputVl(self.getDestinedVl(), \
                                packet[IP].dst, packet[UDP].dport)
        if port != None:
            self.conf_vl = port

    def __getitem__(self, item):
        return self.__packet[item]

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
            #afdxLogger.error("Packet has no sequence number. Not an AFDX packet")
            pass

    def getPayload(self):
        payload = self.__packet[Raw].load
        return payload

    def setPayload(self, payload):
        self.__packet[Raw].load = payload

    def getRawPacket(self):
        return self.__packet
