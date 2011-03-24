from com.afdxsuite.scripts import Script
from com.afdxsuite.config.parsers.icdparser import PORT_QUEUING
from com.afdxsuite.config.parsers import ICD_INPUT_VL
from com.afdxsuite.application.utilities import buildFragmentedMessage,\
    pollForResponse
from com.afdxsuite.config import Factory
from com.afdxsuite.core.network import NETWORK_AB, NETWORK_A, NETWORK_B
from com.afdxsuite.application.commands.RRPC import RRPC

class Script021(Script):
    application = None
    
    def __init__(self, application):
        self.application = application
        self.network = application.network
        super(Script021, self).__init__("ITR-ES-021", has_sequences = True)
        self.input_ports = self.getPorts({'port_characteristic' : PORT_QUEUING,
                                          'ip_frag_allowed' : True,
                                          'network_id' : NETWORK_A},
                                         ICD_INPUT_VL)
        self.input_ports = self.remove_common_ports(self.input_ports)

    def do_operation(self, networks):
        if len(self.input_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        for port in self.input_ports:
            message = buildFragmentedMessage(port, len(networks), "Big message")
            outport = Factory.WRITE(port.RX_AFDX_port_id, message)

            self.application.transmitter.transmit(outport, networks)

            rrpc = RRPC(port)
            self.send(rrpc.buildCommand(), port)
            pollForResponse('RRPC')

    def sequence1(self):
        self.captureForSequence(1)
        self.sendRSET()
        networks = [NETWORK_AB, NETWORK_A, NETWORK_B, NETWORK_A, NETWORK_B]
        self.do_operation(networks)

    def sequence2(self):
        self.captureForSequence(2)
        self.sendRSET()
        networks = [NETWORK_A, NETWORK_B, NETWORK_AB]
        self.do_operation(networks)

    def sequence3(self):
        self.captureForSequence(3)
        self.sendRSET()
        networks = [NETWORK_B, NETWORK_A, NETWORK_AB]
        self.do_operation(networks)

    def run(self):
        self.logger.info("Started sequence 1")
        self.sequence1()
        self.logger.info("Completed sequence 1")

        self.logger.info("Started sequence 2")
        self.sequence2()
        self.logger.info("Completed sequence 2")
        
        self.logger.info("Started sequence 3")
        self.sequence3()
        self.logger.info("Completed sequence 3")
