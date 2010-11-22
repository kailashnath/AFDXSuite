from com.afdxsuite.scripts import Script
from com.afdxsuite.config.parsers import ICD_INPUT_VL
from com.afdxsuite.application.properties import get
from com.afdxsuite.core.network.scapy import conf
from com.afdxsuite.config import Factory

class Script018(Script):
    application = None
    def __init__(self, application):
        self.application = application
        super(Script018, self).__init__("ITR-ES-018")
        self.snmp_ports = self.getPorts({'udp_dst' : int(get("SNMP_UDP_PORT"))},
                                         ICD_INPUT_VL)

    def sendWrongSNMP(self, snmp_port):
        snmp_errcode = conf.mib['afdxICMPInErrors'] + ".0"
        snmp_errcode = snmp_errcode.replace('11348.1', '11348.9')
        outport = Factory.WRITE(snmp_port.RX_AFDX_port_id, "")
        setattr(outport, 'oids', [snmp_errcode])
        setattr(outport, 'proto', 'SNMP')
        self.application.transmitter.transmit(outport, self.network)

    def run(self):
        self.sendRSET()
        for port in self.snmp_ports:
            self.sendWrongSNMP(port)
