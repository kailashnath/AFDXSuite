from com.afdxsuite.scripts import Script
from com.afdxsuite.config.parsers import ICD_ICMP, ICD_INPUT_VL
from com.afdxsuite.core.network import NETWORK_A
from com.afdxsuite.config import Factory
from com.afdxsuite.application.utilities import buildStaticMessage, \
buildFragmentedMessage
from com.afdxsuite.core.network.scapy import conf, ICMP
from com.afdxsuite.application.properties import get

class Script017(Script):
    application = None
    def __init__(self, application):
        self.application = application
        self.network = NETWORK_A
        super(Script017, self).__init__('ITR-ES-017', has_sequences = True)
        self.icmp_ports  = self.getPorts({}, ICD_ICMP)
        self.snmp_ports = self.getPorts(
                                    {'udp_dst' : int(get('SNMP_UDP_PORT'))}, \
                                        ICD_INPUT_VL)
        map(lambda port : setattr(port, 'buffer_size', \
                                                    port.rx_vl_buff_size),\
                                                    self.icmp_ports)

    def sendSNMP(self):
        if len(self.snmp_ports) == 0:
            self.logger.info("Skipping sending SNMP as no SNMP ports found")
            return
        snmp_errcode = conf.mib['afdxICMPInErrors'] + ".0"
        snmp_port = self.snmp_ports[0]
        outport = Factory.WRITE(snmp_port.RX_AFDX_port_id, "")
        setattr(outport, 'oids', [snmp_errcode])
        setattr(outport, 'proto', 'SNMP')
        self.application.transmitter.transmit(outport, self.network)

    def __sendicmp(self, port, message, poll = True):
        self.sendICMP(port, message, poll)

    def sequence1(self):
        self.captureForSequence(1)
        self.sendRSET(poll = True)
        sizes = (64, 65, 80)
        for port in self.icmp_ports:
            for size in sizes:
                self.sendSNMP()
                message = buildStaticMessage(size, "Size = %d" % size)
                self.__sendicmp(port, message, poll = False)
        

    def sequence2(self):
        self.captureForSequence(2)
        self.sendRSET(poll = True)

        for port in self.icmp_ports:
            self.sendSNMP()
            message = buildStaticMessage(64, "Wrong type field")
            port = Factory.WRITE_ICMP(port.rx_vl_id, message)
            packet = self.application.transmitter.transmit(port, self.network, \
                                                           send = False)[0]
            packet[ICMP].code = 1
            self.application.transmitter.transmit_packets([packet], 
                                                          self.network)

    def sequence3(self):
        self.captureForSequence(3)
        self.sendRSET(poll = True)
        for port in self.icmp_ports:
            message = buildStaticMessage(64, "Test")
            count = 150
            while count > 0:
                self.__sendicmp(port, message, poll = False)
                count -= 1

            self.sendICMP(port, "ES Test ping")
            # removed as per Fabienne's comments
            # self.sendSNMP()

    def sequence4(self):
        self.captureForSequence(4)
        self.sendRSET(poll = True)
        for port in self.icmp_ports:
            message = buildFragmentedMessage(port, 2, "Fragmented")
            count = 150
            while count > 0:
                outport = Factory.WRITE_ICMP(port.rx_vl_id, message)
                packet = self.application.transmitter.transmit(outport, 
                                                                self.network,
                                                                send = False)[0]
                self.application.transmitter.transmit_packets([packet], 
                                                          self.network)
                count -= 1
            self.sendICMP(port, "ES Test ping")
            # removed as per Fabienne's comments
            # self.sendSNMP()

    def run(self):
        self.logger.info("Starting sequence 1")
        self.sequence1()
        self.logger.info("Completed sequence 1")
        self.logger.info("Starting sequence 2")
        self.sequence2()
        self.logger.info("Completed sequence 2")
        self.logger.info("Starting sequence 3")
        self.sequence3()
        self.logger.info("Completed sequence 3")
        self.logger.info("Starting sequence 4")
        self.sequence4()
        self.logger.info("Completed sequence 4")
