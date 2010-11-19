from com.afdxsuite.scripts import Script
from com.afdxsuite.core.network import NETWORK_A, NETWORK_AB
from com.afdxsuite.config.parsers import ICD_INPUT_VL, ICD_OUTPUT_VL
from com.afdxsuite.config.parsers.icdparser import PORT_QUEUING
from com.afdxsuite.application.commands.EIPC import EIPC
from com.afdxsuite.config import Factory
from com.afdxsuite.application.commands.TCRQ import TCRQ
from com.afdxsuite.application.utilities import pollForResponse

class Script011(Script):
    application = None

    def __init__(self, application):
        self.application = application
        self.network = NETWORK_A
        super(Script011, self).__init__("ITR-ES-011")
        self.output_ports = self.getPorts({'network_select' : NETWORK_AB,
                                           'port_characteristic' : PORT_QUEUING},
                                          ICD_OUTPUT_VL)
        #self.output_ports = self.remove_common_ports(self.output_ports)

    def run(self):
        self.logger.info("Starting the script")
        smallest_bag = None
        needed_port = None

        for port in self.output_ports:
            bag = port.bag
            if smallest_bag == None:
                smallest_bag = bag

            if bag <= smallest_bag:
                smallest_bag = bag
                needed_port = port
        if needed_port == None:
            self.logger.error("The ICD has no entries")
            return

        self.sendRSET()
        self.logger.info("Smallest BAG chosen is %s" % smallest_bag)
        self.logger.info("Sending an EIPC HOLD on %s" % \
                         needed_port.tx_AFDX_port_id)
        eipc = EIPC(needed_port)
        self.send(eipc.buildCommand(command = 'HOLD', message = "SN Test"),
                  Factory.GET_TX_Port())
        pollForResponse('EIPC')

        tcrq = TCRQ()
        self.send(tcrq.buildCommand(520), Factory.GET_TX_Port())
        pollForResponse('TCRQ')
        raw_input("Press any key to continue.")
