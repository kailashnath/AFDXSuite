from com.afdxsuite.config.parsers import ICD_INPUT_VL, ICD_OUTPUT_VL, ICD_ICMP
from com.afdxsuite.config.parsers.icdparser import CONFIG_ENTRIES, PORT_SAMPLING

PROCESSED_PORTS = {}

def __get_vl(vlId, dst_ip = None, dst_udp = None, port_id = None,
             type = ICD_INPUT_VL):

    entries = CONFIG_ENTRIES[type]
    for entry in entries:
        if type != ICD_ICMP:

            if entry.vl_id == vlId: 
                if port_id == None:
#                    print entry.ip_dst, dst_ip, entry.udp_dst, dst_udp
                    if entry.ip_dst == dst_ip \
                        and entry.udp_dst == dst_udp:
                        return entry
                else:
                    if type == ICD_INPUT_VL and entry.RX_AFDX_port_id == port_id:
                        return entry
                    elif entry.tx_AFDX_port_id == port_id:
                        return entry
    return None

def __get_port(portId, type):

    entries = CONFIG_ENTRIES[type]
    port_attr_name = "tx_AFDX_port_id" if type == ICD_OUTPUT_VL \
                                        else "RX_AFDX_port_id"
    for entry in entries:

        if getattr(entry, port_attr_name) == portId:
            return entry
    return None

def __get_sap_port(sapSrcPort, type):
    entries = CONFIG_ENTRIES[type]
    for entry in entries:
        if entry.udp_src == sapSrcPort:
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

def WRITE_Sap(sapSrcPort, payload, ipDest, udpDest):
    port = __get_sap_port(sapSrcPort, ICD_OUTPUT_VL)

    setattr(port, 'payload', payload)
    port.ip_dst = ipDest
    port.udp_dst = udpDest
    __set_port(port, port.tx_AFDX_port_id, ICD_OUTPUT_VL)
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

def GET_InputVl(vlId, dst_ip, dst_udp):
    return __get_vl(vlId, dst_ip = dst_ip, dst_udp = int(dst_udp), 
                    type = ICD_INPUT_VL)

def GET_ICMPVl(vlId, ip_dst, udp_dst):
    return __get_vl(vlId, ICD_ICMP)

def GET_OutputVl(vlId, afdxPortId):
    return __get_vl(vlId, port_id = int(afdxPortId), type = ICD_OUTPUT_VL)

def GET_Port_Input(portId):
    return __get_port(portId, ICD_INPUT_VL)

def GET_Port_Output(portId):
    return __get_port(portId, ICD_OUTPUT_VL)

def RESET():
    global PROCESSED_PORTS
    PROCESSED_PORTS.clear()
