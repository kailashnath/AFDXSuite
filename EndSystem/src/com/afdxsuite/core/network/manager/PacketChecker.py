from com.afdxsuite.config.parsers import ICD_ICMP
from com.afdxsuite.core.network.scapy import IP, checksum, Packet, UDP, ICMP,\
    Raw
from com.afdxsuite.core.network.snmp.SNMP import SNMP
from com.afdxsuite.core.network.snmp import SNMP_IP_MIB_CODE, SNMP_FRAG_MIB_CODE,\
    SNMP_UDP_MIB_CODE
from com.afdxsuite.config.parsers.icdparser import PORT_SAMPLING

class PacketChecker(object):
    __packet = None
    __conf   = None
    __valid  = False

    def __init__(self, afdxPacket):
        self.__packet = afdxPacket
        if self.__packet != None:
            self.__conf   = self.__packet.conf_vl
            self.runChecks()

    def __ethernetCheck(self):
        return True
        if self.__packet.port_name != ICD_ICMP:
            mfs = self.__conf.max_frame_size
        else:
            mfs = self.__conf.rx_vl_mfs
        if len(self.__packet) > mfs:
            pass

    def __ipCheck(self):
        ip = self.__packet[IP]

        # ip layer checks
        if ip.version != 4 or ip.ihl != 5 or ip.proto not in (1, 17) or \
        ip.chksum == 0:
            SNMP.incrementMIB(SNMP_IP_MIB_CODE)
            return False

        return True                    

    def __udpCheck(self):
        packet = self.__packet
        port   = packet.conf_vl

        if packet[UDP].chksum != 0:
            print 'packet has no udp checksum as 0'
            SNMP.incrementMIB(SNMP_UDP_MIB_CODE)
            return False
        else:

            if port.port_characteristic == PORT_SAMPLING:
                if (packet[UDP].len - 8) != port.buffer_size:
                    print 'Data size != buffer size for packet with Id',\
                    packet[IP].id
                    SNMP.incrementMIB(SNMP_UDP_MIB_CODE)
                    return False
            else:
                if (packet[UDP].len - 8) > port.buffer_size:
                    print 'Data size > buffer size for packet with Id', \
                    packet[IP].id, packet[UDP].len, port.buffer_size
                    SNMP.incrementMIB(SNMP_UDP_MIB_CODE)
                    return False
        return True

    def __icmpCheck(self):
        icmp = self.__packet[ICMP]
        if icmp.type != 8 or len(self.__packet[Raw].load) not in (1, 64):
            print 'ICMP check failed'
            SNMP.incrementMIB(SNMP_IP_MIB_CODE)
            return False
        return True

    def runChecks(self):
        if self.__ethernetCheck() and self.__ipCheck():
            if self.__packet[UDP] != None:
                self.__valid = self.__udpCheck()
            elif self.__packet[ICMP] != None:
                self.__valid = self.__icmpCheck()

    def isPassed(self):
        return self.__valid
