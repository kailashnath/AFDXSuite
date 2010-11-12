from com.afdxsuite.core.network.scapy import IP, defragment
from com.afdxsuite.models.AFDXPacket import AFDXPacket

class FragmentationHandler(object):
    __fragmented_packets = {}
    __packet = None
    __fragmented = False
    __isaFragmentedPacket = False

    def __init__(self):
        pass

    def putPacket(self, packet):
        self.__packet = packet
        ipId = packet[IP].id

        # if this condition is true, it means the packet is fragmented
        if packet[IP].flags == 3:
            self.__isaFragmentedPacket = True
            if self.__fragmented_packets.has_key(ipId):
                self.__fragmented_packets[ipId].append(packet.getRawPacket())
            else:
                self.__fragmented_packets[ipId] = [packet.getRawPacket()]

        elif packet[IP].flags == 2:
            self.__isaFragmentedPacket = False
            if self.__fragmented_packets.has_key(ipId):
                self.__fragmented_packets[ipId].append(packet.getRawPacket())
                defragmented_packet = defragment(self.__fragmented_packets[ipId])
                self.__fragmented_packets[ipId] = defragmented_packet
        else:
            self.__isaFragmentedPacket = False
    
    def getPacket(self):
        ipId = self.__packet[IP].id

        if not self.__isaFragmentedPacket:

            if self.__fragmented_packets.has_key(ipId):
                return AFDXPacket(self.__fragmented_packets.pop(ipId)[0])
            else:
                return self.__packet
