from com.afdxsuite.scripts import Script
from com.afdxsuite.core.network import NETWORK_A
from com.afdxsuite.config.parsers import ICD_OUTPUT_VL, ICD_INPUT_VL
from com.afdxsuite.application.commands.RRPC import RRPC
from com.afdxsuite.application.utilities import buildShortMessage,\
    pollForResponse, buildBigMessage
from com.afdxsuite.config import Factory

import time
from com.afdxsuite.config.parsers.icdparser import PORT_SAMPLING, PORT_QUEUING,\
    PORT_SAP
from com.afdxsuite.application.commands.ESAP import ESAP
from com.afdxsuite.application.properties import get

class Script006(Script):
    application = None

    def __init__(self, application):
        self.application = application
        self.network = NETWORK_A
        super(Script006, self).__init__("ITR-ES-006")
        self.input_ports = self.getPorts({'network_id' : 
                                           self.network.split('&')}, 
                                           ICD_INPUT_VL)
        self.input_ports = self.remove_common_ports(self.input_ports)

    def sequence1(self):
        self.sendRSET()
        for port in self.input_ports:
            rrpc = RRPC( port)
            for count in range(0, 4):
                message = "Message %d" % count
                message = buildShortMessage(port, message)
                self.send(message, port)
                if count == 0 or count == 3:
                    self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
                if count <= 1:
                    self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
                elif count == 2:
                    continue
                #pollForResponse('RRPC')
    
    def sequence2(self):
        self.sendRSET()
        for port in self.input_ports:
            if port.port_characteristic != PORT_SAMPLING:
                continue
            self.logger.info("Testing port %s" % port.RX_AFDX_port_id)
            rrpc = RRPC( port)
            message = "PortId = %d" % port.RX_AFDX_port_id
            message = buildShortMessage(port, message)
            self.send(message, port)
            time.sleep(1) 
            self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
            self.logger.info("Sending RRPC command")
            self.logger.info("Sleeping for 10 seconds")
            time.sleep(10)
            self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
    
    def sequence3(self):
        self.sendRSET()
        for port in self.input_ports:
            if port.port_characteristic != PORT_QUEUING:
                continue
            rrpc = RRPC(port)
            self.send(rrpc.buildCommand(), port)
            for count in range(0, 3):
                message = buildShortMessage(port, "Message = %s" % count)
                self.send(message, port)
            for count in range(0, 3):
                self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
                pollForResponse('RRPC')

    def sequence4(self):
        self.sendRSET()
        for port in self.input_ports:
            if port.port_characteristic != PORT_QUEUING:
                continue
            message = buildBigMessage(port, "Big message")
            self.send(message, port)
            rrpc = RRPC(port)
            self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
            pollForResponse('RRPC')

    def sequence5(self):
        self.sendRSET()
        for port in self.input_ports:
            if port.port_characteristic != PORT_SAP:
                continue
            message = buildShortMessage(port, "PortId = %s" % \
                                        port.RX_AFDX_port_id)
            esap = ESAP(port)
            setattr(port, "ip_dst", get("TE_IP"))
            setattr(port, "udp_dst", int(get("TE_UDP")))
            self.send(esap.buildCommand(message = message))
            pollForResponse('ESAP')

    def run(self):
        self.sequence1()
        self.sequence2()
        self.sequence3()
        self.sequence4()
        self.sequence5()
