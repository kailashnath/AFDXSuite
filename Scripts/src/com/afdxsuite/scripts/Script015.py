from com.afdxsuite.scripts import Script
from com.afdxsuite.config.parsers import ICD_INPUT_VL, ICD_OUTPUT_VL
from com.afdxsuite.config.parsers.icdparser import PORT_QUEUING
from com.afdxsuite.core.network import NETWORK_A, NETWORK_B, NETWORK_AB
import time
from com.afdxsuite.application.commands.RRPC import RRPC
from com.afdxsuite.config import Factory
from com.afdxsuite.application.commands.EIPC import EIPC
from com.afdxsuite.application.utilities import pollForResponse,\
    buildShortMessage


class Script015(Script):
    application = None
    def __init__(self, application):
        self.application = application
        super(Script015, self).__init__("ITR-ES-015", has_sequences = True)
        self.input_ports = self.getPorts({'port_characteristic' : \
                                          PORT_QUEUING}, ICD_INPUT_VL)
        self.input_ports = self.remove_common_ports(self.input_ports)

    def sendOnDisconnectedInterface(self, rx_port, tx_port):
        self.sendRSET()
        self.network = NETWORK_AB
        self.logger.info("Checking the transmission port")
        eipc = EIPC(tx_port)
        message = "PortId = %s" % tx_port.tx_AFDX_port_id
        message = buildShortMessage(tx_port, message)      
        self.send(eipc.buildCommand(message = message), Factory.GET_TX_Port())
        pollForResponse('EIPC')

        self.logger.info("Checking the reception port")
        message = "PortId = %s" % rx_port.RX_AFDX_port_id
        message = buildShortMessage(rx_port, message)
        self.send(message, rx_port)
        rrpc = RRPC(rx_port)
        self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
        pollForResponse('RRPC')

    def getrxtxports(self):
        self.output_ports = self.getPorts({}, ICD_OUTPUT_VL)
        self.input_ports = self.getPorts({}, ICD_INPUT_VL)
        rx_ports = self.remove_common_ports(self.input_ports)
        tx_ports = self.remove_common_ports(self.output_ports)
        if len(rx_ports) == 0 or len(tx_ports) == 0:
            self.logger.error("This icd has no ports required by the sequence")
            return
        rx_port = rx_ports[0]
        tx_port = tx_ports[0]
        return (rx_port, tx_port)

    def sequence1(self):
        self.captureForSequence(1)
        if len(self.input_ports) == 0:
            self.logger.error("The ICD has no ports satisfying the scripts "\
                              "criteria")
            return
        self.sendRSET()
        port = self.input_ports[0]
        skews = [port.skew_max, port.skew_max + 1000,  port.skew_max - 1000]
        for skew in skews:
            message = buildShortMessage(port, "Skew = %d" % skew)
            sleep_time_micros = float(skew)/1000
            self.logger.info("Sending packet with skew of %d ms" % \
                             sleep_time_micros)
            networks = [NETWORK_A, NETWORK_B]
            if sleep_time_micros < 65.5:
                networks.reverse()

            for network in networks:
                self.network = network
                self.send(message, port)
                time.sleep(float(sleep_time_micros)/1000)

            self.logger.info("Sending an RRPC")
            rrpc = RRPC(port)
            self.network = NETWORK_A
            self.send(rrpc.buildCommand(), Factory.GET_TX_Port())

    def sequence2(self):
        self.captureForSequence(2)
        raw_input("Do a hard reset of the ES and press any key to continue")
        self.sequence1()

    def sequence3(self):
        self.captureForSequence(3)
        raw_input('Disconnect A network physically and press enter to continue')
        rx_port, tx_port = self.getrxtxports()
        self.sendOnDisconnectedInterface(rx_port, tx_port)

    def sequence4(self):
        self.captureForSequence(4)
        raw_input('Disconnect B network physically and press enter to continue')
        rx_port, tx_port = self.getrxtxports()
        self.sendOnDisconnectedInterface(rx_port, tx_port)


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
