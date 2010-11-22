from com.afdxsuite.scripts import Script
from com.afdxsuite.core.network import NETWORK_AB

from com.afdxsuite.config.parsers import ICD_INPUT_VL
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
        self.network = NETWORK_AB
        super(Script006, self).__init__("ITR-ES-006", has_sequences = True)
        self.input_ports = self.getPorts({'network_id' : 
                                           self.network.split('&')}, 
                                           ICD_INPUT_VL)
        self.input_ports = self.remove_common_ports(self.input_ports)

    def sequence1(self):
        self.captureForSequence(1)
        if len(self.input_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.sendRSET()
        for port in self.input_ports:
            rrpc = RRPC( port)

            for count in range(0, 4):
                message = "Message %d" % count
                message = buildShortMessage(port, message)
                self.send(message, port)
                self.logger.info("Filling the port %s" % port.RX_AFDX_port_id)
                if count == 0 or count == 3:
                    self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
                    self.logger.info("Sending an RRPC")
                if count <= 1:
                    self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
                    self.logger.info("Sending an RRPC")
                elif count == 2:
                    continue
                pollForResponse('RRPC')
    
    def sequence2(self):
        self.captureForSequence(2)
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
        self.captureForSequence(3)
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
        self.captureForSequence(4)
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
        self.captureForSequence(5)
        self.sendRSET()
        for port in self.input_ports:
            if port.port_characteristic != PORT_SAP:
                continue
            message = buildShortMessage(port, "PortId = %s" % \
                                        port.RX_AFDX_port_id)
            setattr(port, "ip_dst", get("TE_IP"))
            setattr(port, "udp_dst", int(get("TE_UDP")))
            esap = ESAP(port)
            self.send(esap.buildCommand(message = message))
            pollForResponse('ESAP')

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
