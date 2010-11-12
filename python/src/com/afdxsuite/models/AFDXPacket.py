from com.afdxsuite.core.network.scapy import Ether
from com.afdxsuite.config import Factory

class AFDXPacket(object):
    __packet = None
    __conf_vl = None

    def __init__(self, packet):
        self.__packet = packet
        self.__conf_vl = Factory.GET_InputVl(self.getDestinedVl())

    def getDestinedVl(self):
        dst_mac = self.__packet[Ether].dst
        vl_id = (str(dst_mac)[-5:]).replace(':', '')
        return int(vl_id, 16)
        
        