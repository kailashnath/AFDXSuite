from com.afdxsuite.scripts import Script
from com.afdxsuite.core.network import NETWORK_A
from com.afdxsuite.config.parsers import ICD_OUTPUT_VL
from com.afdxsuite.application.commands.EIPC import EIPC
from com.afdxsuite.config import Factory
from com.afdxsuite.application.commands.TCRQ import TCRQ
from com.afdxsuite.application.utilities import pollForResponse,\
    buildShortMessage

class Script012(Script):
    application = None

    def __init__(self, application):
        self.application = application
        self.network = application.network
        super(Script012, self).__init__("ITR-ES-012")
        self.output_ports = self.getPorts({'network_id' : NETWORK_A}, ICD_OUTPUT_VL)
        self.output_ports = self.remove_common_ports(self.output_ports)

    def run(self):
        if len(self.output_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.sendRSET()
        for port in self.output_ports:
            eipc = EIPC(port)
            self.logger.info("Sending EIPC HOLD on %s" % \
                             port.tx_AFDX_port_id)
            self.send(eipc.buildCommand(command = 'HOLD',\
                                        message = buildShortMessage(port,
                                                    "RM test",
                                                    eipc.command_size)), 
                                        Factory.GET_TX_Port())
            pollForResponse("EIPC")

        tcrq = TCRQ()
        self.logger.info("Seding a TCRQ for %d times" % 2)
        self.send(tcrq.buildCommand(2), Factory.GET_TX_Port())
        raw_input("Press enter key to continue.....")
