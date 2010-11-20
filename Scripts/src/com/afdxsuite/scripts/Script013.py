from com.afdxsuite.scripts import Script
from com.afdxsuite.core.network import NETWORK_AB, NETWORK_A, NETWORK_B
from com.afdxsuite.config.parsers import ICD_INPUT_VL
from com.afdxsuite.application.utilities import buildShortMessage,\
    pollForResponse, buildFragmentedMessage
from com.afdxsuite.application.commands.RRPC import RRPC
from com.afdxsuite.config import Factory
from com.afdxsuite.config.parsers.icdparser import PORT_QUEUING, PORT_SAMPLING

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
        print 'SN = ', sn
        return sn

    def send_modified_snpackets(self, ports, networks):
        for port in ports:
            for network in networks:
                message = "PortId = %s %s" % (port.RX_AFDX_port_id, network)
                message = buildShortMessage(port, message)

                outport = Factory.WRITE(port.RX_AFDX_port_id, message)
                setattr(outport, 'sn_func', self.sn_modifier)

                self.application.transmitter.transmit(outport, network)
                rrpc = RRPC(port)
                self.network = NETWORK_A
                self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
                #pollForResponse('RRPC')

    def send_modified_snfragments(self, ports, networks):
        for port in ports:
            message = "PortId = %s" % port.RX_AFDX_port_id
            message = buildFragmentedMessage(port, len(networks), message)
            outport = Factory.WRITE(port.RX_AFDX_port_id, message)
            setattr(outport, 'sn_func', self.sn_modifier)
            self.application.transmitter.transmit(outport, networks)
            rrpc = RRPC(port)
            self.network = NETWORK_A
            self.send(rrpc.buildCommand(), Factory.GET_TX_Port())

    def sequence1(self):
        #self.sendRSET()
        for port in self.input_ports:
            for network in [NETWORK_AB, NETWORK_A, NETWORK_B]:
                message = "PortId = %s %s" % (port.RX_AFDX_port_id, network)
                message = buildShortMessage(port, message)
                self.network = network
                self.send(message, port)

                rrpc = RRPC(port)
                self.network = NETWORK_A
                self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
                #pollForResponse('RRPC')

    def sequence2(self):
        #self.sendRSET()
        ports = []
        for port in self.input_ports:
            if port.ic_active == False:
                continue
            ports.append(port)
        networks = [NETWORK_AB, NETWORK_A, NETWORK_B,NETWORK_A, NETWORK_B]
        self.send_modified_snpackets(ports, networks)

    def sequence3(self):
        self.sendRSET()
        ports = []
        for port in self.input_ports:
            if port.ic_active == False or \
            port.port_characteristic == PORT_SAMPLING:
                continue
            ports.append(port)
        networks = [NETWORK_AB, NETWORK_A, NETWORK_B, NETWORK_A, NETWORK_B]
        self.send_modified_snfragments(ports, networks)

    def sequence4(self):
        self.sendRSET()
        ports = []
        for port in self.input_ports:
            if port.ic_active == True:
                continue
            ports.append(port)
        networks = [NETWORK_AB, NETWORK_A, NETWORK_B, NETWORK_A, NETWORK_B]
        self.send_modified_snpackets(ports, networks)


    def sequence5(self):
        pass

    def run(self):
        self.sequence3()
