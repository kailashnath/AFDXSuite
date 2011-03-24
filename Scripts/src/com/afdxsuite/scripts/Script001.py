from com.afdxsuite.scripts import Script
from com.afdxsuite.config import Factory
from com.afdxsuite.config.parsers import ICD_OUTPUT_VL
from com.afdxsuite.application.utilities import pollForResponse
from com.afdxsuite.application.commands.EIPC import EIPC
from com.afdxsuite.core.network import NETWORK_A
from com.afdxsuite.config.parsers.icdparser import PORT_SAMPLING, PORT_QUEUING

class Script001(Script):
    application = None

    def __init__(self, application):
        super(Script001, self).__init__("ITR-ES-001")
        self.network = application.network
        self.ports = self.getPorts({'network_id' : NETWORK_A,
                                    'port_characteristic' : \
                                          [PORT_SAMPLING, PORT_QUEUING]},
                                    ICD_OUTPUT_VL)

        self.ports = self.remove_common_ports(self.ports)
        self.application = application

    def run(self):

        if len(self.ports) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.sendRSET()

        for port in self.ports:
            eipc = EIPC(port)
            message = "PortId = %s" % port.tx_AFDX_port_id
            command = eipc.buildCommand(messagetype = 'U', message = message)

            self.logger.info("Sending an EIPC request on port : %s" % \
                             port.tx_AFDX_port_id)

            self.send(command, Factory.GET_TX_Port())

            if not pollForResponse("EIPC"):
                self.logger.error("The ES has not responded for EIPC")

    def test(self):
        pass

    def stop(self):
        super(Script001, self).stop()
