from com.afdxsuite.core.network import NETWORK_A, NETWORK_B
from com.afdxsuite.core.network.scapy import Ether, sendp, IP, UDP, Raw, ICMP,\
    SNMP, Padding, fragment
from com.afdxsuite.application.properties import get
from com.afdxsuite.core.network.utils import SequenceHandler

class TransmitHandler(object):
    __network = None

    def __init__(self, network):
        self.__network = network
        self._sn_handler = SequenceHandler()

    def __addEthernetDetails(self):
        eth = Ether()
        src_mac_padding = '%04x' % self.__port.vl_id
        eth.dst = "%s:%s:%s" % (get("MAC_PREFIX_RX"), 
                                                 src_mac_padding[:2], 
                                                 src_mac_padding[2:])
        eth.src = get("MAC_PREFIX_TX") + ":20"
        eth.type = 0x800
        self.__packet = eth

    def __addIpDetails(self):
        port = self.__port
        ip_layer = IP()
        ip_layer.src = port.ip_src if hasattr(port, 'ip_src') else \
            get("TE_IP_" + self.__network)
        ip_layer.dst = port.ip_dst
        ip_layer.id  = self._sn_handler.nextIpId()
        #ip_layer.prot = 0x17
        self.__packet = self.__packet/ip_layer

    def __addUDPDetails(self):
        port = self.__port

        udp_layer = UDP()
        udp_layer.sport = port.udp_src if hasattr(port, 'udp_src') else \
        int(get("TE_UDP"))
        udp_layer.dport = port.udp_dst
        udp_layer.chksum = 0x00
        #udp_layer.len    = len(port.payload)
        self.__packet = self.__packet/udp_layer

    def __addPayload(self):
        self.__packet /= self.__port.payload

    def __normalize(self):
        port = self.__port

        # any payload size greater than 1472 needs to be fragmented
        # as the its the ethernet limitation
        if len(port.payload) > 1472 or len(port.payload) > port.max_frame_size:
            self.__packet = self.fragment(self.__packet)
        else:
            self.__packet = [self.__packet]

    def __addPadding(self, packet):
        if packet[SNMP] != None:
            payload_length = packet[UDP].len - 8
        else:
            payload_length = len(packet[Raw])

        padding = ''
        # the size index 17 is caculated as 60 - (ethHdr + ipHdr + udpHdr) = 18
        # but here we are using the size index as 17 because the last bit will
        # be the sequence number which will be added at 'transmit' function

        if payload_length < 17:
            padding = '\0' * (17 - payload_length)

        sn = self._sn_handler.next(self.__port.vl_id)
        if sn == 0:
            padding += '\0'
        else:
            padding += chr(sn)

        packet /= Padding(padding)
        return packet

    def __createPacket(self):
        if self.__port == None:
            return
        if (not hasattr(self.__port, 'payload')) or self.__port.payload == None:
            return
        self.__addEthernetDetails()
        self.__addIpDetails()
        self.__addUDPDetails()
        self.__addPayload()
        self.__normalize()

    def transmit(self, port, network = None):
        self.__port = port
        self.__createPacket()

        if network == None:
            network = self.__network

        for packet in self.__packet:
            packet = self.__addPadding(packet)

            if NETWORK_A in network:
                packet[Ether].src = get("MAC_PREFIX_TX") + ":20"
                sendp(packet, iface = get("NETWORK_INTERFACE_A"),
                      verbose = False)
            if NETWORK_B in network:
                packet[Ether].src = get("MAC_PREFIX_TX") + ":40"
                sendp(packet, iface = get("NETWORK_INTERFACE_B"),
                      verbose = False)

    def fragment(self, packet):
        max_frame_size = 1472 if self.__port.max_frame_size > 1472 else \
        self.__port.max_frame_size 
        if max_frame_size < len(packet[Raw].load):
            return fragment(packet, max_frame_size)
        else:
            return [packet]
