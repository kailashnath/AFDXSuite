from com.afdxsuite.scripts import Script
from com.afdxsuite.config.parsers.icdparser import PORT_SAP
from com.afdxsuite.config.parsers import ICD_INPUT_VL
from com.afdxsuite.application.properties import get
from com.afdxsuite.config import Factory
from com.afdxsuite.application.utilities import getMIBOIDBySize, getMIBOID
from com.afdxsuite.core.network import NETWORK_A

import time

class Script024(Script):
    def __init__(self, application):
        self.application = application
        self.network = application.network
        super(Script024, self).__init__("ITR-ES-024")
        self.snmp_ports = self.getPorts({'port_characteristic' : PORT_SAP,
                                         'udp_dst' : int(get('SNMP_UDP_PORT'))},
                                          ICD_INPUT_VL)

    def sendSNMP(self, snmp_port, oids, snmp_type = 0):
        outport = Factory.WRITE(snmp_port.RX_AFDX_port_id, 
                                reduce(lambda x,y : x + y, oids))
        setattr(outport, 'oids', oids)

        if snmp_type == 1:
            setattr(outport, 'proto', 'SNMPnext')
        else:
            setattr(outport, 'proto', 'SNMP')

        self.application.transmitter.transmit(outport, self.network)

    def run(self):
        dummy_port = None

        if len(self.snmp_ports) == 0:
            self.logger.error("The ICD has no ports satisfying the sequence" \
                              " criteria. Hence sending from a dummy SNMP port")
            dummy_port = (Factory.GET_SNMP_DummyPort(),)
            self.snmp_ports = dummy_port

        self.sendRSET()
        for rxPort in self.snmp_ports:
            oid_1 = getMIBOID('afdxEquipmentStatus')
            oids_4kb = getMIBOIDBySize(220)
            oids_8kb = getMIBOIDBySize(452)
            self.logger.info("Sending an SNMP get request")
            self.sendSNMP(rxPort, [oid_1])
            self.logger.info("Sending an SNMP get request of " \
                                "size ~4Ko")
            self.sendSNMP(rxPort, oids_4kb)
            self.logger.info("Sending an SNMP get request of " \
                                "size ~8Ko")
            self.sendSNMP(rxPort, oids_8kb)

        if dummy_port:
            Factory.REM_Port(dummy_port[0])

        if get('SNMP_TRAPS_ENABLED').lower() == 'true':
                self.logger.info("Listening for traps. Duration : 10 seconds")
                time.sleep(10)

