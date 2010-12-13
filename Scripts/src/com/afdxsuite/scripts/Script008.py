from com.afdxsuite.core.network import NETWORK_AB
from com.afdxsuite.config.parsers import ICD_ICMP, ICD_INPUT_VL
from com.afdxsuite.scripts import Script
from com.afdxsuite.application.utilities import buildMessage, pollForResponse,\
    buildShortMessage
from com.afdxsuite.config import Factory

class Script008(Script):
    application = None

    def __init__(self, application):
        self.application = application
        self.network = NETWORK_AB
        super(Script008, self).__init__("ITR-ES-008", has_sequences = True)
        self.icmp_ports = self.getPorts({}, ICD_ICMP)
        self.input_port = self.getPorts({}, ICD_INPUT_VL)
        self.logger.info("Starting script ITR-ES-008")
        self.input_port = self.remove_common_ports(self.input_port)

    def __sendicmp(self, port, message, poll = True):
        self.logger.info("Sending an ICMP message on %s" % port.rx_vl_id)
        port = Factory.WRITE_ICMP(port.rx_vl_id, message)
        self.application.transmitter.transmit(port, self.network)
        if poll:
            pollForResponse(message, timeout = 1)

    def sequence1(self):
        self.captureForSequence(1)
        for port in self.icmp_ports:
            setattr(port, 'buffer_size', port.rx_vl_buff_size)
            for size in range(1, 65):
                message = buildMessage(port, size)
                self.__sendicmp(port, message)

    def sequence2(self):
        if len(self.input_port) == 0:
            self.logger.info("There are no ports in the ICD satisfying the " \
                             "scripts criteria")
            return
        self.captureForSequence(2)
        index = 0
        self.network = 'A'
        for port in self.input_port:
            message = buildShortMessage(port, "Background message")
            self.send(message, port)
            if index % 3 == 0:
                for icmp_port in self.icmp_ports:
                    setattr(icmp_port, 'buffer_size', icmp_port.rx_vl_buff_size)
                    message = buildMessage(icmp_port, 64)
                    self.__sendicmp(icmp_port, message, poll = False)
            index += 1

    def run(self):
        self.logger.info("Starting sequence 1")
        self.sequence1()
        self.logger.info("Completed sequence 1")

        self.logger.info("Starting sequence 2")
        self.sequence2()
        self.logger.info("Completed sequence ")
