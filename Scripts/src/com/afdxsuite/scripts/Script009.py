from com.afdxsuite.scripts import Script
from com.afdxsuite.core.network import NETWORK_A, NETWORK_B, NETWORK_AB
from com.afdxsuite.config.parsers.icdparser import PORT_QUEUING
from com.afdxsuite.config.parsers import ICD_INPUT_VL
from com.afdxsuite.application.utilities import buildFragmentedMessage, \
pollForResponse
from com.afdxsuite.config import Factory
from com.afdxsuite.application.commands.RRPC import RRPC

class Script009(Script):
    application = None

    def __init__(self, application):
        self.application = application
        self.network = application.network
        super(Script009, self).__init__("ITR-ES-009", has_sequences = True)
        self.input_ports = self.getPorts({'port_characteristic' : PORT_QUEUING,
                                          'network_id' : NETWORK_A},
                                          ICD_INPUT_VL)
        self.input_ports = self.remove_common_ports(self.input_ports)

    def sendMessage(self, seqNo, ports, networks):
        if len(ports) == 0 :
            self.logger.error("This sequence cannot proceed as there are no" \
                              " ports in the ICD satisfying the sequence" \
                              " requirements")
            return

        self.captureForSequence(seqNo)
        self.sendRSET()
        pollForResponse('OK')

        for port in ports:
            message = buildFragmentedMessage(port, 6, message = "Fragmented")
            outPort = Factory.WRITE(port.RX_AFDX_port_id, message)
            self.application.transmitter.transmit(outPort, \
                                          network = networks)
            rrpc = RRPC(port)
            self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
            pollForResponse('RRPC')

    def sequence1(self):
        networks = [NETWORK_A, NETWORK_B] * 3
        ports = []
        for port in self.input_ports:
            if port.rma == True and port.ip_frag_allowed == True:
                ports.append(port)

        self.sendMessage(1, ports, networks)

    def sequence2(self):
        ports = []
        for port in self.input_ports:
            if port.rma == False and port.ip_frag_allowed == True:
                ports.append(port)

        self.sendMessage(2, ports, [NETWORK_A, NETWORK_B] * 3)

    def sequence3(self):
        ports = []

        for port in self.input_ports:
            if port.rma == True and port.ip_frag_allowed == True:
                ports.append(port)

        self.sendMessage(3, ports, [NETWORK_AB] + [NETWORK_A, NETWORK_B] * 2 + \
                         [NETWORK_AB])

    def sequence4(self):
        ports = []
        for port in self.input_ports:
            if port.rma == True and port.ip_frag_allowed == True:
                ports.append(port)

        self.sendMessage(4, ports, [NETWORK_A, NETWORK_B, NETWORK_AB] * 2)

    def sequence5(self):
        ports = []
        for port in self.input_ports:
            if port.rma == True and port.ip_frag_allowed == True:
                ports.append(port)

        self.sendMessage(5, ports, [NETWORK_B, NETWORK_A, NETWORK_AB] * 2)

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

        self.logger.info("Starting sequence 5")
        self.sequence5()
        self.logger.info("Completed sequence 5")
