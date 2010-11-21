from com.afdxsuite.core.network import scapy
from com.afdxsuite.core.network.scapy import SNMPvarbind, IP, UDP, SNMPget,\
    SNMPresponse, ASN1_OID, SNMPnext
from com.afdxsuite.config import Factory
from com.afdxsuite.core.network.hooks.snmp import oid_value_mapping

class SNMP(object):

    __command = None
    __application = None
    __port = None
    __destinationPort = 162

    def __init__(self, application, snmpPacket):
        self.__application = application
        self.__port = Factory.GET_InputVl(snmpPacket.getDestinedVl(),
                                          snmpPacket[IP].dst,
                                          snmpPacket[UDP].dport)

        if snmpPacket[scapy.SNMP] == None:
            return

        self.__command = snmpPacket
        self.buildResponse()

    def __getOID(self):
        request = self.__command[SNMPget]
        oids = []

        if request == None:
            request = self.__command[SNMPnext]

        if request != None:
            varlist = request.varbindlist

            for varbind in varlist:
                oids.append(varbind.oid.val)             
            return oids
        
        return self.__command[SNMPvarbind].oid.val

    def __getOIDValue(self, oid):
        oid = oid[:-2]
        return oid_value_mapping[oid]

    def __getNextOIDValue(self, oid):
        # incomplete need to be implemented
        oid = oid[:-2]
        while True:
            oid_arr = oid.split('.')
            next_oid = int(oid_arr[-1]) + 1
            
            if oid_value_mapping.has_key(next_oid):
                oid_arr[-1] = next_oid
                next_oid = ".".join(oid_arr)
                return oid_value_mapping[next_oid]
            else:
                pass

    def buildResponse(self):
        oids = self.__getOID()
        if type(oids) == list:
            _varbindlist = [SNMPvarbind(oid = ASN1_OID(oid),
                                         value = self.__getOIDValue(oid)) \
                            for oid in oids]
        else:
            _varbindlist = [SNMPvarbind(oid = ASN1_OID(self.__getOID()),
                                        value = 1)]

        response = scapy.SNMP(community = "afdxRead",
                               PDU = SNMPresponse(varbindlist = _varbindlist))

        port = Factory.WRITE(self.__port.RX_AFDX_port_id, response)
        port.ip_dst = self.__command[IP].src
        port.udp_dst = self.__destinationPort
        self.__application.transmit(port)

    @staticmethod
    def incrementMIB(trapCode):
        print 'trap', trapCode

