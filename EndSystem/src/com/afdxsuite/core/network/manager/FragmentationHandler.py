from com.afdxsuite.core.network.scapy import IP, defragment, UDP
from com.afdxsuite.models.AFDXPacket import AFDXPacket
from com.afdxsuite.core.network.snmp.SNMP import SNMP
from com.afdxsuite.core.network.snmp import SNMP_IP_MIB_CODE, SNMP_FRAG_MIB_CODE
from com.afdxsuite.config.parsers.icdparser import PORT_SAMPLING

class FragmentationHandler(object):
    __fragmented_packets = {}
    __packet = None
    __fragmented = False
    __isPacketValid = False
    __isaFragmentedPacket = False
    __udpPorts = list()

    def __init__(self):
        pass

    def __basicChecks(self, packet):
        #fragmentation checks
        if packet[IP].flags != 0:
            if hasattr(packet.conf_vl, 'port_characteristic'):
                if packet.conf_vl.port_characteristic == PORT_SAMPLING: 
                    SNMP.incrementMIB(SNMP_FRAG_MIB_CODE)
                    return False
        return True
        if (packet[IP].dst != packet.conf_vl.ip_dst):
            print packet[IP].dst, packet.conf_vl.ip_dst
            SNMP.incrementMIB(SNMP_FRAG_MIB_CODE)
            return False

        return True

    def __checkFragmentedPacket(self, packet):
        id = packet[IP].id
        if id not in self.__fragmented_packets.keys():
            SNMP.incrementMIB(SNMP_FRAG_MIB_CODE)
            print 'fail at check frag'
            return False

        return True

    def __checkDefragmentedPacket(self, packet):
        offset_val     = packet[IP].frag << 3
        payload_length = packet[IP].len
        if (offset_val + payload_length) != (packet[UDP].len - 8):
            SNMP.incrementMIB(SNMP_IP_MIB_CODE)
            return False
        return True

    def putPacket(self, packet):
        """The variable packet here is an instance of AFDXPacket"""
        self.__packet = packet
        ipId = packet[IP].id

        if not self.__basicChecks(self.__packet):

            self.__isPacketValid = False
            return

        # the below condition is true if the packet has more fragments MF
        # and is a fragmented packet
        if packet[IP].flags == 3:
            self.__isaFragmentedPacket = True

            # if the fragment is the first fragment
            if (packet[IP].frag << 3) == 0:
                self.__fragmented_packets[ipId] = list(packet.getRawPacket())
                return

            if(self.__checkFragmentedPacket(packet)):
                self.__fragmented_packets[ipId].append(packet.getRawPacket())
            else:
                self.__isPacketValid = False

        # the below condition is true if the packet is the last fragment of
        # a set of fragmented packets DF
        elif packet[IP].flags == 2:
            self.__isaFragmentedPacket = False
            if self.__fragmented_packets.has_key(ipId):
                self.__fragmented_packets[ipId].append(packet.getRawPacket())
                defragmented_packet = \
                    defragment(self.__fragmented_packets[ipId])
                if self.__checkDefragmentedPacket(defragmented_packet[0]):
                    self.__isPacketValid = True
                self.__fragmented_packets[ipId] = defragmented_packet


        # the packet is a normal packet
        else:
            self.__isaFragmentedPacket = False
            self.__isPacketValid = True

    def getPacket(self):
        ipId = self.__packet[IP].id

        if not self.__isaFragmentedPacket and self.__isPacketValid:

            if self.__fragmented_packets.has_key(ipId):
                return AFDXPacket(self.__fragmented_packets.pop(ipId)[0])
            else:
                return self.__packet

    def reset(self):
        self.__fragmented_packets.clear()
        self.__udpPorts = list()
        self.__packet = None
        self.__fragmented = False
        self.__isPacketValid = False
        self.__isaFragmentedPacket = False
