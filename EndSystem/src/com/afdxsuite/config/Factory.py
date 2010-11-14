from com.afdxsuite.config.parsers import ICD_INPUT_VL, ICD_OUTPUT_VL, ICD_ICMP
from com.afdxsuite.config.parsers.icdparser import CONFIG_ENTRIES, PORT_SAMPLING

PROCESSED_PORTS = {}

def __get_vl(vlId, type):

    entries = CONFIG_ENTRIES[type]
    for entry in entries:
        if type != ICD_ICMP:
            if entry.vl_id == vlId:
                return entry
        else:
            

def __get_port(portId, type):

    entries = CONFIG_ENTRIES[type]
    port_attr_name = "tx_AFDX_port_id" if type == ICD_OUTPUT_VL \
                                        else "RX_AFDX_port_id"
    for entry in entries:
        if getattr(entry, port_attr_name) == portId:
            return entry
    return None

def __set_port(newport, portId, type):
    entries = CONFIG_ENTRIES[type]
    port_attr_name = "tx_AFDX_port_id" if type == ICD_OUTPUT_VL \
                                        else "RX_AFDX_port_id"
    for entry in entries:
        if getattr(entry, port_attr_name) == portId:
            CONFIG_ENTRIES[type].remove(entry)
            CONFIG_ENTRIES[type].append(newport)

def __get_processed_packet(portId):
    global PROCESSED_PORTS
    return PROCESSED_PORTS.get(portId)

def __get_ports(icd_type, port_type):
    entries = CONFIG_ENTRIES[icd_type]
    result_ports = list()

    for entry in entries:
        if entry.port_characteristic == port_type:
            result_ports.append(entry)
    return result_ports

def put_processed_packet(afdxPacket):
    global PROCESSED_PORTS
    portId = afdxPacket.conf_vl.RX_AFDX_port_id
    PROCESSED_PORTS[portId] = afdxPacket

def WRITE(afdxPortId, payload):
    port = __get_port(afdxPortId, ICD_OUTPUT_VL)
    setattr(port, 'payload', payload)
    __set_port(port, afdxPortId, ICD_OUTPUT_VL)
    return port

def WRITE_Sap(sapPortId, payload, ipDest, udpDest):
    port = __get_port(sapPortId, ICD_OUTPUT_VL)
    setattr(port, 'payload', payload)
    port.ip_dst = ipDest
    port.udp_dst = udpDest
    __set_port(port, sapPortId, ICD_OUTPUT_VL)
    return port

def READ(portId):

    packet = __get_processed_packet(portId)
    if packet != None:
        payload = packet.getPayload()
        if packet.conf_vl.port_characteristic == PORT_SAMPLING:
            packet.setPayload(None)
            put_processed_packet(packet)

        return payload
    return None

def READ_Sampling(samplingPortId):
    return READ(samplingPortId)

def READ_Queuing(queuingPortId):
    return READ(queuingPortId)

def GET_InputVl(vlId):
    return __get_vl(vlId, ICD_INPUT_VL)

def GET_ICMPVl(vlId):
    return __get_vl(vlId, ICD_ICMP)

def GET_OutputVl(vlId):
    return __get_vl(vlId, ICD_OUTPUT_VL)

def GET_Port_Input(portId):
    return __get_port(portId, ICD_INPUT_VL)

def GET_Port_Output(portId):
    return __get_port(portId, ICD_OUTPUT_VL)

def RESET():
    global PROCESSED_PORTS
    PROCESSED_PORTS.clear()
