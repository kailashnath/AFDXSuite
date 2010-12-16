from com.afdxsuite.scripts import Script
from com.afdxsuite.core.network import NETWORK_AB, NETWORK_A, NETWORK_B
from com.afdxsuite.config.parsers import ICD_INPUT_VL
from com.afdxsuite.application.utilities import buildShortMessage,\
    pollForResponse, buildFragmentedMessage
from com.afdxsuite.application.commands.RRPC import RRPC
from com.afdxsuite.config import Factory
from com.afdxsuite.config.parsers.icdparser import PORT_SAMPLING

class Script013(Script):
    application = None
    def __init__(self, application):
        self.application = application
        super(Script013, self).__init__("ITR-ES-013", has_sequences = True)
        self.input_ports = self.getPorts({},
                                         ICD_INPUT_VL)
        self.input_ports = self.remove_common_ports(self.input_ports)
        self.__sns = {}

    def sn_modifier(self, vl_id):
        if self.__sns.has_key(vl_id):
            sn = self.__sns[vl_id] + 3
        else:
            sn = 2
        self.__sns[vl_id] = sn

        return sn

    def send_modified_snpackets(self, ports, networks):
        if len(ports) == 0:
            self.logger.error("There are no ports in the icd file satisfying" \
                              " this criteria. Hence quitting the sequence")
            return
        self.sendRSET()
        for port in ports:
            for network in networks:
                message = "PortId = %s %s" % (port.RX_AFDX_port_id, network)
                message = buildShortMessage(port, message)

                outport = Factory.WRITE(port.RX_AFDX_port_id, message)
                setattr(outport, 'sn_func', self.sn_modifier)
                self.application.transmitter.transmit(outport, network)
                self.logger.info("Filling rx port : %s" % port.RX_AFDX_port_id)
                rrpc = RRPC(port)
                self.network = NETWORK_A
                self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
                self.logger.info("Sending an RRPC on network %s" % self.network)
                pollForResponse('RRPC')

    def send_modified_snfragments(self, ports, networks):
        self.sendRSET()
        for port in ports:
            message = "PortId = %s" % port.RX_AFDX_port_id
            message = buildFragmentedMessage(port, len(networks), message)
            outport = Factory.WRITE(port.RX_AFDX_port_id, message)
            setattr(outport, 'sn_func', self.sn_modifier)
            self.application.transmitter.transmit(outport, networks)
            self.logger.info("Filling rx port : %s" % port.RX_AFDX_port_id)
            rrpc = RRPC(port)
            self.network = NETWORK_A
            self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
            self.logger.info("Sending an RRPC on network %s" % self.network)
            pollForResponse('RRPC')

    def sequence1(self):
        if len(self.input_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.captureForSequence(1)
        self.sendRSET()
        for port in self.input_ports:
            self.logger.info("Filling rx port : %s" % port.RX_AFDX_port_id)
            for network in [NETWORK_AB, NETWORK_A, NETWORK_B]:
                message = "PortId = %s %s" % (port.RX_AFDX_port_id, network)
                message = buildShortMessage(port, message)
                self.network = network
                self.send(message, port)

                rrpc = RRPC(port)
                self.network = NETWORK_A
                self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
                self.logger.info("Sending an RRPC on network %s" % network)
                pollForResponse('RRPC')

    def sequence2(self):
        if len(self.input_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.captureForSequence(2)
        ports = []
        for port in self.input_ports:
            if port.ic_active == False:
                continue
            ports.append(port)
        networks = [NETWORK_AB, NETWORK_A, NETWORK_B,NETWORK_A, NETWORK_B]
        self.send_modified_snpackets(ports, networks)

    def sequence3(self):
        if len(self.input_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.captureForSequence(3)
        ports = []
        for port in self.input_ports:
            if port.ic_active == False or \
            port.port_characteristic == PORT_SAMPLING:
                continue
            ports.append(port)
        networks = [NETWORK_AB, NETWORK_A, NETWORK_B, NETWORK_A, NETWORK_B]
        self.send_modified_snfragments(ports, networks)

    def sequence4(self):
        if len(self.input_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.captureForSequence(4)
        ports = []
        for port in self.input_ports:
            if port.ic_active == True:
                continue
            ports.append(port)
        networks = [NETWORK_AB, NETWORK_A, NETWORK_B, NETWORK_A, NETWORK_B]
        self.send_modified_snpackets(ports, networks)


    def sequence5(self):
        if len(self.input_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.captureForSequence(5)
        ports = []
        for port in self.input_ports:
            if port.ic_active == True:
                continue
            ports.append(port)
        networks = [NETWORK_AB, NETWORK_A, NETWORK_B, NETWORK_A, NETWORK_B]
        self.send_modified_snfragments(ports, networks)

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
