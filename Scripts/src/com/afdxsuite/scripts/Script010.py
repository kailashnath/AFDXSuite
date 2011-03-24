from com.afdxsuite.scripts import Script
from com.afdxsuite.core.network import NETWORK_A
from com.afdxsuite.config.parsers.icdparser import PORT_SAMPLING, PORT_QUEUING
from com.afdxsuite.config.parsers import ICD_INPUT_VL, ICD_OUTPUT_VL
from com.afdxsuite.application.utilities import buildStaticMessage, \
pollForResponse
from com.afdxsuite.application.commands.EIPC import EIPC
from com.afdxsuite.config import Factory
from com.afdxsuite.application.commands.RRPC import RRPC

class Script010(Script):
    application = None

    def __init__(self, application):
        self.application = application
        self.network = application.network
        super(Script010, self).__init__("ITR-ES-010", has_sequences = True)
        self.input_ports = self.getPorts({'port_characteristic' : \
                                          [PORT_SAMPLING, PORT_QUEUING],
                                          'network_id' : NETWORK_A},
                                          ICD_INPUT_VL)
        self.input_ports = self.remove_common_ports(self.input_ports)
        self.output_ports = self.getPorts({'port_characteristic' : \
                                          [PORT_SAMPLING, PORT_QUEUING],
                                          'network_id' : NETWORK_A},
                                          ICD_OUTPUT_VL)
        self.output_ports = self.remove_common_ports(self.output_ports)

    def sequence1(self):
        if len(self.input_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.captureForSequence(1)
        self.sendRSET()
        for port in self.output_ports:
            if port.ip_frag_allowed:
                continue
            eipc = EIPC(port)
            message = buildStaticMessage(int(port.max_frame_size), \
                                         "MFS + 1")
            self.send(eipc.buildCommand(message = message), \
                      Factory.GET_TX_Port())
            self.logger.info("Sending an EIPC command on port : %s" % \
                             port.tx_AFDX_port_id)
            pollForResponse('EIPC')

    def sequence2(self):
        if len(self.input_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.captureForSequence(2)
        self.sendRSET()
        ports = []
        for port in self.input_ports:
            if port.rma:
                continue
            ports.append(port)
        if len(ports) < 1:
            self.logger.error("There are no ICD entries which have rma" \
                              " as inactive")
            return
        for port in ports:
            message = buildStaticMessage(port.max_frame_size + 2, "Frag")
            outPort = Factory.WRITE(port.RX_AFDX_port_id, message)
            self.application.transmitter.transmit(outPort, \
                                                  network = [NETWORK_A, 'C'])
            rrpc = RRPC(port)
            self.send(rrpc.buildCommand(), port)

    def run(self):
        self.logger.info("Starting sequence 1")
        self.sequence1()
        self.logger.info("Completed sequence 1")
        self.logger.info("Starting sequence 2")
        self.sequence2()
        self.logger.info("Completed sequence 2")
