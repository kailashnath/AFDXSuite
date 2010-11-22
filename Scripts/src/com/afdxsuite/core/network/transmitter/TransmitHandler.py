from com.afdxsuite.core.network import NETWORK_A, NETWORK_B, scapy
from com.afdxsuite.core.network.scapy import Ether, sendp, IP, UDP, Raw, ICMP,\
    SNMP, Padding, fragment, SNMPvarbind, ASN1_OID, SNMPresponse, SNMPnext,\
    SNMPget
from com.afdxsuite.application.properties import get
from com.afdxsuite.core.network.utils import SequenceHandler
from com.afdxsuite.application.utilities import i2h

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
            get("TE_IP")
        ip_layer.dst = port.ip_dst
        ip_layer.id  = self._sn_handler.nextIpId()
        ip_layer.ttl = 1
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

    def __addICMP(self):
        port = self.__port
        icmp = ICMP()
        icmp.seq = self._sn_handler.next(port.rx_vl_id)
        self.__packet /= icmp

    def __addSNMP(self):

        oids = self.__port.oids
        varbindlist = [SNMPvarbind(oid = \
                                   ASN1_OID(str(oid).replace("enterprises", \
                                                             "1.3.6.1.4.1"))) \
                                                             for oid in oids]
        if 'next' in self.__port.proto:
            pdu = SNMPnext(varbindlist = varbindlist)
        else:
            pdu = SNMPget(varbindlist = varbindlist)

        snmp_packet = scapy.SNMP(community = "afdxRead", PDU = pdu)
        #print "Packet length is ", len(reduce(lambda x,y : 
        #                                      str(x).replace('.', '') + 
        #                                      str(y).replace('.', ''), oids))
        self.__packet /= snmp_packet

    def __addPayload(self):
        if 'SNMP' in self.__port.proto:
            self.__addSNMP()
        else:
            self.__packet /= self.__port.payload

    def __normalize(self):
        port = self.__port
        # any payload size greater than 1472 needs to be fragmented
        # as the its the ethernet limitation
        if (len(port.payload) > 1472 or \
            len(port.payload) > int(port.max_frame_size)):
            self.__packet = self.fragment(self.__packet)
        else:
            self.__packet = [self.__packet]

    def __addPadding(self, packet):
        if packet[SNMP] != None:
            return packet
            #payload_length = packet[UDP].len - 8
        else:
            payload_length = len(packet[Raw])

        padding = ''
        # the size index 17 is caculated as 60 - (ethHdr + ipHdr + udpHdr) = 18
        # but here we are using the size index as 17 because the last bit will
        # be the sequence number which will be added at 'transmit' function

        if payload_length < 17:
            padding = '\0' * (17 - payload_length)

        if hasattr(self.__port, 'sn_func'):
            sn = self.__port.sn_func(self.__port.vl_id)
        else:
            sn = self._sn_handler.next(self.__port.vl_id)
        if sn == 0:
            padding += '\0'
        else:
            padding += ('\\x%02X' % sn).decode('string_escape')

        packet /= Padding(padding)
        return packet

    def __createPacket(self):
        if self.__port == None:
            return
        if (not hasattr(self.__port, 'payload')) or self.__port.payload == None:
            return

        self.__addEthernetDetails()
        self.__addIpDetails()
        if self.__port.proto in ('UDP', 'SNMP', 'SNMPnext'):
            self.__addUDPDetails()
        elif self.__port.proto == 'ICMP':
            self.__addICMP()

        self.__addPayload()
        self.__normalize()

    def change_sequence_number(self, to_seqno, vlId):
        self._sn_handler.change_sn(to_seqno, vlId)

    def transmit(self, port, network = None, send = True):
        def transmit_low(packet, network):
            packet = self.__addPadding(packet)
            packets = []

            if NETWORK_A in network:
                packet[Ether].src = get("MAC_PREFIX_TX") + ":20"
                if send:
                    sendp(packet, iface = get("NETWORK_INTERFACE_A"),
                          verbose = False)
                else:
                    packets.append(packet)
            if NETWORK_B in network:
                packet[Ether].src = get("MAC_PREFIX_TX") + ":40"
                if send:
                    sendp(packet, iface = get("NETWORK_INTERFACE_B"),
                          verbose = False)
                else:
                    packets.append(packet)
            return packets

        self.__port = port
        self.__createPacket()

        if network == None:
            network = self.__network

        packets = []

        if type(network) == list:
            if len(network) == len(self.__packet):
                for index in range(0, len(network)):
                    network_id = network[index]
                    packet = self.__packet[index]
                    packets += transmit_low(packet, network_id)
        else:
            for packet in self.__packet:
                packets += transmit_low(packet, network)
        if not send:
            return packets

    def transmit_packets(self, packets, network):
        for packet in packets:
            if NETWORK_A in network:
                packet[Ether].src = get("MAC_PREFIX_TX") + ":20"
                sendp(packet, iface = get("NETWORK_INTERFACE_A"),
                      verbose = False)
            if NETWORK_B in network:
                packet[Ether].src = get("MAC_PREFIX_TX") + ":40"
                sendp(packet, iface = get("NETWORK_INTERFACE_B"),
                      verbose = False)

    def fragment(self, packet):

        max_frame_size = 1472 if int(self.__port.max_frame_size) > 1472 else \
        int(self.__port.max_frame_size) 
        if (packet[Raw] != None and  max_frame_size < len(packet[Raw].load)) or\
        (packet[SNMP] != None and max_frame_size < len(packet[SNMP])):
            return fragment(packet, max_frame_size)
        else:
            return [packet]
