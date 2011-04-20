from com.afdxsuite.scripts import Script
from com.afdxsuite.core.network import NETWORK_A, NETWORK_AB
from com.afdxsuite.config.parsers import ICD_INPUT_VL
from com.afdxsuite.application.commands.ERPQ import ERPQ
from com.afdxsuite.config import Factory
from com.afdxsuite.application.utilities import buildShortMessage,\
    pollForResponse
from com.afdxsuite.application.commands.RRPC import RRPC
from com.afdxsuite.core.network.scapy import IP, Ether, UDP, TCP

class Script016(Script):
    application = None
    def __init__(self, application):
        self.application = application
        self.network = NETWORK_AB
        super(Script016, self).__init__("ITR-ES-016")
        self.input_ports = self.getPorts({'network_id' : NETWORK_A},
                                          ICD_INPUT_VL)
        self.input_ports = self.remove_common_ports(self.input_ports)

    def send_packet(self, packet):
        if packet != None:
            self.application.transmitter.transmit_packets([packet],
                                                          self.network)

    def get_packet(self, port, message):
        self.logger.info("Sending packet with : %s" % message)
        outport = Factory.WRITE(port.RX_AFDX_port_id, message)
        return self.application.transmitter.transmit(outport,
                                                     network = self.network,
                                                     send = False)[0]


    def run(self):
        if len(self.input_ports) == 0:
            self.logger.error("The ICD has no ports satisfying the scripts "\
                              "criteria")
        self.sendRSET()
        port = self.input_ports[0]
        erpq = ERPQ(port)
        self.send(erpq.buildCommand(), Factory.GET_TX_Port())
        feature_index = 0
        pollForResponse('ERPQ')

        def sendRRPC():
            rrpc = RRPC(port)
            self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
            pollForResponse('RRPC')

        while feature_index < 20:
            if feature_index in (0, 1, 15, 17, 19): 
                message = buildShortMessage(port, message = "Normal Frame")
                self.send(message, port)
                sendRRPC()
            elif feature_index == 2:
                message = buildShortMessage(port, message = "Wrong ip version")
                packet = self.get_packet(port, message)
                packet[IP].version = 15
                self.send_packet(packet)
                sendRRPC()
            elif feature_index == 3:
                message = buildShortMessage(port, message = "Wrong ihl")
                packet = self.get_packet(port, message)
                packet[IP].ihl = 5
                self.send_packet(packet)
                sendRRPC()
            elif feature_index == 4:
                message = buildShortMessage(port, message = "Wrong tos")
                packet = self.get_packet(port, message)
                packet[IP].tos = 4
                self.send_packet(packet)
                sendRRPC()
            elif feature_index == 5:
                message = buildShortMessage(port, message = "Wrong ctrl flag")
                packet = self.get_packet(port, message)
                packet[IP].flags = 0x03
                self.send_packet(packet)
                sendRRPC()
            elif feature_index == 6:
                message = buildShortMessage(port, message = "Wrong ttl field")
                packet = self.get_packet(port, message)
                packet[IP].ttl = 0
                self.send_packet(packet)
                sendRRPC()
            elif feature_index == 7:
                message = buildShortMessage(port, message = "Wrong ttl field")
                packet = self.get_packet(port, message)
                packet[IP].ttl = 2
                self.send_packet(packet)
                sendRRPC()
            elif feature_index == 8:
                message = buildShortMessage(port, message = "Wrong checksum "\
                                            "field")
                packet = self.get_packet(port, message)
                packet[IP].chksum = 0x01
                self.send_packet(packet)
                sendRRPC()
            elif feature_index == 9:
                message = buildShortMessage(port, message = "Wrong ip  dest")
                packet = self.get_packet(port, message)
                packet[IP].dst = '1.2.3.4'
                self.send_packet(packet)
                sendRRPC()
            elif feature_index == 10:
                message = buildShortMessage(port, message = "Wrong ip  dest")
                packet = self.get_packet(port, message)
                packet[IP].dst = '255.255.255.255'
                self.send_packet(packet)
                sendRRPC()
            elif feature_index == 11:
                message = buildShortMessage(port, message = "Wrong ip dest cst")
                packet = self.get_packet(port, message)
                dst = packet[IP].dst
                if str(dst).startswith('10.'):
                    dst = str(dst).replace('10.', '120.')
                elif str(dst).startswith('224.224'):
                    dst = str(dst).replace('224.224', '234.234')
                packet[IP].dst = dst
                self.send_packet(packet)
                sendRRPC()
            elif feature_index == 12:
                message = buildShortMessage(port, message = "Wrong mac cst")
                packet = self.get_packet(port, message)
                dst = packet[Ether].dst
                if str(dst).startswith('03:00:00'):
                    dst = dst.replace('03:00:00', '03:01:01')
                packet[Ether].dst = dst
                self.send_packet(packet)
                sendRRPC()
            elif feature_index == 13:
                message = buildShortMessage(port, message = "Wrong mac type "\
                                            "field")
                packet = self.get_packet(port, message)
                packet[Ether].type = 0x0002
                self.send_packet(packet)
                sendRRPC()
            elif feature_index == 14:
                message = buildShortMessage(port, message = "Wrong IP options "\
                                            "in header")
                packet = self.get_packet(port, message)
                packet[IP].options = 'dummy'
                self.send_packet(packet)
                sendRRPC()
            elif feature_index == 16:
                message = buildShortMessage(port, message = "Wrong udp "\
                                            "checksum field")
                packet = self.get_packet(port, message)
                packet[UDP].chksum = 0x03
                self.send_packet(packet)
                sendRRPC()
            elif feature_index == 18:
                packet = self.get_packet(port, message)
                mac_dst = packet[Ether].dst
                mac_src = packet[Ether].src
                ip_dst = packet[IP].dst
                ip_src = packet[IP].src
                pckt = Ether(dst = mac_dst, src = mac_src) \
                       /IP(dst = ip_dst,  src = ip_src) \
                       /TCP(sport = 50205, dport = port.udp_dst) \
                       /"TCP fragment"
                self.send_packet(pckt)
                sendRRPC()
            feature_index += 1
