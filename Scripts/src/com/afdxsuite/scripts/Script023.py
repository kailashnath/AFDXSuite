from com.afdxsuite.scripts import Script
from com.afdxsuite.config.parsers.icdparser import PORT_SAP
from com.afdxsuite.application.properties import get
from com.afdxsuite.config import Factory
from com.afdxsuite.application.utilities import getMIBOID, getAFDXEquipmentGroup,\
    getAFDXMACGroup, getAFDXIPGroup, getAFDXUDPGroup, getAFDXESFailureGroup,\
    buildShortMessage, getMIBOIDBySize
from com.afdxsuite.config.parsers import ICD_INPUT_VL

import random, copy, time

class Script023(Script):
    application = None
    def __init__(self, application):
        self.application = application
        super(Script023, self).__init__("ITR-ES-023", has_sequences = True)
        self.sap_ports = self.getPorts({'port_characteristic' : PORT_SAP,
                                        'udp_dst' : int(get('SNMP_UDP_PORT'))},
                                       ICD_INPUT_VL)
        self.input_ports = self.getPorts({}, ICD_INPUT_VL)
        self.input_ports = self.remove_common_ports(self.input_ports)

    def sendSNMP(self, snmp_port, oids, snmp_type = 0):
        outport = Factory.WRITE(snmp_port.RX_AFDX_port_id, 
                                reduce(lambda x,y : x + y, oids))
        setattr(outport, 'oids', oids)

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
            
            oids = [getMIBOID('afdxMACStatus', 1), 
                    getMIBOID('afdxMACStatus', 2)] 
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
            
            oids_4kb = getMIBOIDBySize(220)
            oids_8kb = getMIBOIDBySize(452)

            self.sendSNMP(port, oids_4kb, 1)
            self.sendSNMP(port, oids_8kb, 1)

    def sequence3(self):
        if len(self.sap_ports) == 0 or len(self.input_ports) == 0:
            self.logger.error("The ICD has no ports satisfying the sequence" \
                              " criteria")
            return
        self.captureForSequence(3)
        self.sendRSET()
        message = "Traffic"
        sap_ports = copy.deepcopy(self.sap_ports)
        while True:
            if len(sap_ports) == 0:
                break
            for _ in range(0, 10):
                port = self.input_ports[random.randint(0, 
                                                    len(self.input_ports) - 1)]
                message = buildShortMessage(port, message)
                self.send(message, port)
                if _%5 == 0:
                    sap_port = sap_ports.pop()
    
                    oid_4kb = getMIBOIDBySize(220)
                    self.sendSNMP(sap_port, oid_4kb, 1)


    def sequence4(self):
        if len(self.sap_ports) == 0:
            self.logger.error("The ICD has no ports satisfying the sequence" \
                              " criteria")
            return
        self.captureForSequence(4)
        self.sendRSET()
        start = time.time()
        while True:
            for port in self.sap_ports:
                oid_8kb = getMIBOIDBySize(452)
                self.logger.info("Sending SNMP whose size is nearly equal to "\
                                 "8KB sisze")
                self.sendSNMP(port, oid_8kb, 1)
            if time.time() - start > 10:
                break

    def run(self):
        self.logger.info("Starting sequence 1")
        self.sequence1()
        self.logger.info("Completed sequence 1")
        self.logger.info("Started sequence 2")
        self.sequence2()
        self.logger.info("Completed sequence 2")
        self.logger.info("Started sequence 3")
        self.sequence3()
        self.logger.info("Completed sequence 3")
        self.logger.info("Started sequence 4")
        self.sequence4()
        self.logger.info("Completed sequence 4")
