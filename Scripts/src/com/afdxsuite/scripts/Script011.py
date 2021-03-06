from com.afdxsuite.scripts import Script
from com.afdxsuite.core.network import NETWORK_A
from com.afdxsuite.config.parsers import ICD_OUTPUT_VL
from com.afdxsuite.config.parsers.icdparser import PORT_QUEUING
from com.afdxsuite.application.commands.EIPC import EIPC
from com.afdxsuite.config import Factory
from com.afdxsuite.application.commands.TCRQ import TCRQ
from com.afdxsuite.application.utilities import pollForResponse

class Script011(Script):
    application = None

    def __init__(self, application):
        self.application = application
        self.network = application.network
        super(Script011, self).__init__("ITR-ES-011")
        self.output_ports = self.getPorts({'network_id' : NETWORK_A,
                                           'port_characteristic' : PORT_QUEUING},
                                          ICD_OUTPUT_VL)
        self.output_ports = self.remove_common_ports(self.output_ports)

    def run(self):
        self.logger.info("Starting the script")
        smallest_bag = None
        needed_port = None
        if len(self.output_ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
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
        self.send(tcrq.buildCommand(257), Factory.GET_TX_Port())
        self.logger.info("Sending a TCRQ command.")
        pollForResponse('TCRQ')
        raw_input("Press enter/return key to continue......")
