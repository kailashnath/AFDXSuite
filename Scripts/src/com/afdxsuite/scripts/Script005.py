from com.afdxsuite.scripts import Script
from com.afdxsuite.core.network import NETWORK_A
from com.afdxsuite.config.parsers.icdparser import PORT_SAP
from com.afdxsuite.config.parsers import ICD_OUTPUT_VL
from com.afdxsuite.application.commands.EIPC import EIPC
from com.afdxsuite.application.utilities import buildMessage, buildShortMessage,\
    pollForResponse
from com.afdxsuite.application.commands.ESAP import ESAP
from com.afdxsuite.application.properties import get
from com.afdxsuite.config import Factory

class Script005(Script):
    application = None
    
    def __init__(self, application):
        self.application = application
        self.network = application.network
        super(Script005, self).__init__("ITR-ES-005")
        self.output_ports = self.getPorts({'network_id' : NETWORK_A},
                                         ICD_OUTPUT_VL)
        self.output_ports = self.remove_common_ports(self.output_ports)

    def run(self):
        self.logger.info("Starting sequence 1")
        if len(self.output_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.sendRSET()
        for port in self.output_ports:
            if port.port_characteristic == PORT_SAP:
                cmd = ESAP(port)
                setattr(port, "ip_dst", get("TE_IP"))
                setattr(port, "udp_dst", int(get("TE_UDP")))
            else:
                #cmd = EIPC(port)
                cmd = ESAP(port)
            command_size = cmd.command_size
            message = "Short message"
            messages = []
            messages.append(buildShortMessage(port, message, command_size))
            messages.append(buildMessage(port, 
                                     (int(port.buffer_size)/2) - command_size, 
                                     message))
            messages.append(buildMessage(port,
                                        int(port.buffer_size) - command_size,
                                        message))
            for message in messages:
                command = cmd.buildCommand(command = 'SEND', message = message)
                self.send(command, Factory.GET_TX_Port())

                if not pollForResponse(("OK", "ERR")):
                    self.logger.info("The ES did not respond to EIPC command")
