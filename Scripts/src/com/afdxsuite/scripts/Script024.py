from com.afdxsuite.scripts import Script
from com.afdxsuite.config.parsers.icdparser import PORT_SAP
from com.afdxsuite.application.properties import get
from com.afdxsuite.config.parsers import ICD_INPUT_VL
from com.afdxsuite.application.utilities import getMIBOID, get4KBOID
from com.afdxsuite.core.network import SNMP_GETNext

class Script024(Script):
    application = None
    def __init__(self, application):
        self.application = application
        super(Script024, self).__init__("ITR-ES-024")
        self.snmp_ports = self.getPorts({'port_characteristic' : PORT_SAP,
                                        'udp_dst' : int(get('SNMP_UDP_PORT'))},
                                       ICD_INPUT_VL)

    def run(self):
        self.sendRSET()
        for port in self.snmp_ports:
            
            oids = getMIBOID('afdxEquipmentStatus')
            self.sendSNMP(port, [oids])
            for _ in range(0, 5):
                oids = get4KBOID()
                self.sendSNMP(port, oids, SNMP_GETNext)
                
                self.sendSNMP(port, oids * 2, SNMP_GETNext)
