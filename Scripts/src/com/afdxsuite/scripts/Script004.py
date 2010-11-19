from com.afdxsuite.scripts import Script
from com.afdxsuite.config.parsers.icdparser import PORT_SAMPLING, PORT_QUEUING
from com.afdxsuite.config.parsers import ICD_OUTPUT_VL
from com.afdxsuite.application.commands.EIPC import EIPC
from com.afdxsuite.application.utilities import buildShortMessage,\
    pollForResponse
from com.afdxsuite.config import Factory
from com.afdxsuite.application.commands.TCRQ import TCRQ

class Script004(Script):
    application = None

    def __init__(self, application):
        self.application = application
        super(Script004, self).__init__("ITR-ES-004")
        self.output_ports = self.getPorts({'network_id' : self.network.split('&'),
                                          'port_characteristic' : \
                                          [PORT_SAMPLING, PORT_QUEUING]},
                                         ICD_OUTPUT_VL)
        self.output_ports = self.remove_common_ports(self.output_ports)

    def run(self):
        self.logger.info("Starting sequence 1")
        self.sendRSET()
        for port in self.output_ports:
            eipc = EIPC(self.application, port)
            message = "PortId = %s" % port.tx_AFDX_port_id
            offset_size = eipc.command_size
            command = eipc.buildCommand(command = 'HOLD',
                                        message = buildShortMessage(port, 
                                                                message, 
                                                                offset_size))
            self.send(command, Factory.GET_TX_Port())
            if not pollForResponse('EIPC'):
                self.logger.error("The ES has not responded to EIPC")

        tcrq = TCRQ()
        self.send(tcrq.buildCommand(10), Factory.GET_TX_Port())
        if not pollForResponse('TCRQ'):
                self.logger.error("The ES has not responded to TCRQ")
        raw_input("Press any key to continue.")
