from com.afdxsuite.scripts import Script
from com.afdxsuite.config.parsers.icdparser import PORT_SAP
from com.afdxsuite.application.properties import get
from com.afdxsuite.config import Factory
from com.afdxsuite.application.utilities import getMIBOID, getAFDXEquipmentGroup,\
    getAFDXMACGroup, getAFDXIPGroup, getAFDXUDPGroup, getAFDXESFailureGroup,\
    getMIBOIDBySize
from com.afdxsuite.config.parsers import ICD_INPUT_VL

class Script023(Script):
    application = None
    def __init__(self, application):
        self.application = application
        super(Script023, self).__init__("ITR-ES-023", has_sequences = True)
        self.sap_ports = self.getPorts({'port_characteristic' : PORT_SAP,
                                        'udp_dst' : int(get('SNMP_UDP_PORT'))},
                                       ICD_INPUT_VL)

    def sendSNMP(self, snmp_port, oids, snmp_type = 0):
        mod_oids = []
        for oid in oids:
            oid = oid + ".0"
            mod_oids.append(oid)
        outport = Factory.WRITE(snmp_port.RX_AFDX_port_id, 
                                reduce(lambda x,y : x + y, mod_oids))
        setattr(outport, 'oids', mod_oids)

        if snmp_type == 1:
            setattr(outport, 'proto', 'SNMPnext')
        else:
            setattr(outport, 'proto', 'SNMP')

        self.application.transmitter.transmit(outport, self.network)


    def sequence1(self):
        if len(self.sap_ports) == 0:
            self.logger.error("The ICD has no ports satisfying the sequence" \
                              " criteria")
            return
        self.captureForSequence(1)
        self.sendRSET()
        for port in self.sap_ports:
            oids = getMIBOID('afdxEquipmentStatus')
            self.sendSNMP(port, [oids])
            
            oids = [getMIBOID('afdxMACStatus', 0), 
                    getMIBOID('afdxMACStatus', 1)] 
            self.sendSNMP(port, oids)

            oids = getAFDXEquipmentGroup() + getAFDXMACGroup()
            self.sendSNMP(port, oids)
            
            oids = getAFDXEquipmentGroup() + getAFDXMACGroup() + \
            getAFDXIPGroup() + getAFDXUDPGroup() + getAFDXESFailureGroup()
            self.sendSNMP(port, oids)


    def sequence2(self):
        if len(self.sap_ports) == 0:
            self.logger.error("The ICD has no ports satisfying the sequence" \
                              " criteria")
            return
        self.captureForSequence(2)
        self.sendRSET()
        for port in self.sap_ports:
            oid = getMIBOID('afdxEquipmentStatus')
            self.sendSNMP(port, [oid])
            
            oid_4kb = getAFDXEquipmentGroup() + getAFDXMACGroup() + \
            getAFDXIPGroup() + getAFDXUDPGroup() + getAFDXESFailureGroup()
            oid_4kb = (oid_4kb * 6) + getAFDXUDPGroup()

            self.sendSNMP(port, oid_4kb, 1)
            
            oid_8kb = oid_4kb * 2
            self.sendSNMP(port, oid_8kb, 1)

    def run(self):
        self.sequence2()
