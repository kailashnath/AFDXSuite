from com.afdxsuite.scripts import Script
from com.afdxsuite.config.parsers import ICD_INPUT_VL, ICD_ICMP
from com.afdxsuite.config.parsers.icdparser import PORT_QUEUING
from com.afdxsuite.application.utilities import buildFragmentedMessage
from com.afdxsuite.config import Factory
from com.afdxsuite.core.network import NETWORK_A

class Script020(Script):
    application = None
    def __init__(self, application):
        self.application = application
        self.network = NETWORK_A
        super(Script020, self).__init__('ITR-ES-020', has_sequences = True)
        self.input_ports = self.getPorts({'ip_frag_allowed' : True,
                                          'network_id' : NETWORK_A,
                                          'port_characteristic' : \
                                          PORT_QUEUING}, ICD_INPUT_VL)
        self.icmp_ports  = self.getPorts({}, ICD_ICMP)
        self.input_ports = self.remove_common_ports(self.input_ports)

    def sequence1(self):
        if len(self.input_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.captureForSequence(1)
        self.sendRSET()
        for port in self.input_ports:
            message = buildFragmentedMessage(port, 5)
            outport = Factory.WRITE(port.RX_AFDX_port_id, message)
            packets = self.application.transmitter.transmit(outport, 
                                                           self.network,
                                                           False)
            self.application.transmitter.transmit_packets(packets[0],
                                                          self.network)
        for port in self.icmp_ports:
            self.sendICMP(port, "Port Test")

    def sequence2(self):
        if len(self.input_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.captureForSequence(2)
        self.sendRSET()
        for port in self.input_ports:
            message = buildFragmentedMessage(port, 5)
            outport = Factory.WRITE(port.RX_AFDX_port_id, message)
            packets = self.application.transmitter.transmit(outport, 
                                                           self.network,
                                                           False)
            for _ in range(0, 5):
                self.application.transmitter.transmit_packets(packets[0],
                                                              self.network)
            self.application.transmitter.transmit_packets(packets[1:],
                                                          self.network)
        for port in self.icmp_ports:
            self.sendICMP(port, "Port Test")

    def run(self):
        self.logger.info("Started sequence 1")
        self.sequence1()
        self.logger.info("Completed sequence 1")
        self.logger.info("Started sequence 2")
        self.sequence2()
        self.logger.info("Completed sequence 2")
