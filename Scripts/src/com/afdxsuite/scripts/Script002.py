from com.afdxsuite.scripts import Script
from com.afdxsuite.config import Factory
from com.afdxsuite.config.parsers import ICD_INPUT_VL
from com.afdxsuite.application.properties import get
from com.afdxsuite.application.commands.RRPC import RRPC
from com.afdxsuite.config.parsers.icdparser import PORT_SAMPLING, PORT_QUEUING
from com.afdxsuite.application.utilities import pollForResponse

class Script002(Script):
    application = None

    def __init__(self, application):
        self.application = application
        super(Script002, self).__init__("ITR-ES-002", has_sequences = True)
        self.network = application.network
        self.input_ports = self.getPorts({'network_id' : self.network,
                                          'port_characteristic' : \
                                          [PORT_SAMPLING, PORT_QUEUING]},
                                         ICD_INPUT_VL)
        self.input_ports = self.remove_common_ports(self.input_ports)

    def __fillRxPorts(self, ports):

        for port in ports:
            if port.udp_dst == int(get("TE_UDP")):
                continue
            message = "Port Id = %s" % port.RX_AFDX_port_id
            self.logger.info("Filling the Rx port %s" % port.RX_AFDX_port_id)
            self.send(message, port)

    def sequence1(self):

        if len(self.input_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.captureForSequence(1)
        self.sendRSET()
        self.__fillRxPorts(self.input_ports)

        for port in self.input_ports:
            rrpc = RRPC(port)
            self.logger.info("Sending RRPC for port = %s" % \
                             port.RX_AFDX_port_id)
            self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
        
            if not pollForResponse("RRPC"):
                self.logger.error("The ES has not responded for RRPC")

    def sequence2(self):
        ports = {}
        atleast_one = False
        if len(self.input_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        for port in self.input_ports:
            key = (port.udp_dst, port.ip_dst)

            if ports.has_key(key):
                port.ip_src = "10.1.33.1"
                ports[key].append(port)
                atleast_one = True
            else:
                port.ip_src = "10.1.33.2"
                ports[key] = [port]
        if not atleast_one:
            self.logger.info("Sequence 2 cannot proceed. ICD has no ports "\
                             "satisfying the script requirements")
            return
        self.captureForSequence(2)
        self.sendRSET()

        for key in ports.keys():
            sel_ports = ports[key]
            if len(sel_ports) > 1:
                self.__fillRxPorts(sel_ports)

                for port in sel_ports:
                    rrpc = RRPC(port)
                    self.send(rrpc.buildCommand(), Factory.GET_TX_Port())

                    if not pollForResponse("RRPC"):
                        self.logger.error("The ES has not responded for RRPC")


    def run(self):
        self.logger.info("Starting sequence 1")
        self.sequence1()
        self.logger.info("Completed sequence 1")
        self.logger.info("Starting sequence 2")
        self.sequence2()
        self.logger.info("Completed sequence 2")
