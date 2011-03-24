from com.afdxsuite.scripts import Script
from com.afdxsuite.config.parsers import ICD_OUTPUT_VL, ICD_INPUT_VL
from com.afdxsuite.application.properties import get
from com.afdxsuite.core.network.scapy import conf
from com.afdxsuite.config import Factory
from com.afdxsuite.application.utilities import buildShortMessage, \
buildStaticMessage
from com.afdxsuite.application.commands.EIPC import EIPC
from com.afdxsuite.config.parsers.icdparser import PORT_QUEUING
from com.afdxsuite.application.commands.RRPC import RRPC
from com.afdxsuite.core.network import NETWORK_A

class Script019(Script):
    application = None
    def __init__(self, application):
        self.application = application
        self.network = NETWORK_A
        super(Script019, self).__init__("ITR-ES-019", has_sequences = True)
        self.output_ports = self.getPorts({}, ICD_OUTPUT_VL)
        self.input_ports = self.getPorts({'port_characteristic' : PORT_QUEUING},
                                          ICD_INPUT_VL)
        self.snmp_ports = self.getPorts({'udp_dst' : int(get("SNMP_UDP_PORT"))},
                                         ICD_INPUT_VL)
        self.output_ports = self.remove_common_ports(self.output_ports)
        self.input_ports = self.remove_common_ports(self.input_ports)

    def sendSNMP(self, snmp_port):
        snmp_errcode = conf.mib['afdxOutLackOfBuffer'] + ".0"
        outport = Factory.WRITE(snmp_port.RX_AFDX_port_id, "")
        setattr(outport, 'oids', [snmp_errcode])
        setattr(outport, 'proto', 'SNMP')
        self.application.transmitter.transmit(outport, self.network)

    def doOperation(self, port, snmp_port):
        eipc = EIPC(port)
        message = buildStaticMessage(port.max_frame_size + 1, "Big message")

        self.sendSNMP(snmp_port)
        self.send(eipc.buildCommand(message), Factory.GET_TX_Port())

        self.sendSNMP(snmp_port)

        message = buildShortMessage(port, "Short message", eipc.command_size)
        self.send(eipc.buildCommand(message), Factory.GET_TX_Port())


    def sequence1(self):
        self.captureForSequence(1)
        self.sendRSET()

        if len(self.output_ports) == 0 or len(self.snmp_ports) == 0:
            self.logger.error("There are no ports in the ICD satisfying the "\
                              "scripts criteria")
            return
        port = self.output_ports[0]
        snmp_port = self.snmp_ports[0]
        self.doOperation(port, snmp_port)
        
    def sequence2(self):
        self.captureForSequence(2)
        seq_port = None

        for port in self.output_ports:
            if port.buffer_size > port.max_frame_size and port.ip_frag_allowed:
                seq_port = port
                break
        if seq_port == None:
            self.logger.error("There is no port in the ICD satisfying the "\
                              "sequence criteria")
            return

        self.sendRSET()
        snmp_port = self.snmp_ports[0]
        self.doOperation(seq_port, snmp_port)

    def sequence3(self):
        self.captureForSequence(3)
        self.sendRSET()
        rx_port = None

        for port in self.input_ports:
            if port.buffer_size == 8192:
                rx_port = port
                break
        if rx_port == None:
            self.logger.error("The ICD has no entries satisfying the "\
                              "sequences criteria")
            return
        message = buildStaticMessage(8192, "Message size = %d" % (8192))
        self.send(message, port)
        rrpc = RRPC(port)
        self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
        
        # even though we set this size as 31, during fragmentation its size
        # becomes 32 as 32 % 8 == 0
        port.max_frame_size = 31
        self.send(message, port)
        self.send(rrpc.buildCommand(), Factory.GET_TX_Port())


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
