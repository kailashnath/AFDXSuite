from com.afdxsuite.config.parsers import ICD_INPUT_VL, ICD_OUTPUT_VL
from com.afdxsuite.config.parsers.icdparser import CONFIG_ENTRIES

PROCESSED_PORTS = {}

def __get_vl(vlId, type):

    entries = CONFIG_ENTRIES[type]

    for entry in entries:
        if entry.vl_id == vlId:
            return entry

def put_processed_packet(afdxPacket):
    global PROCESSED_PORTS
    portId = afdxPacket.conf_vl.RX_AFDX_port_id
    PROCESSED_PORTS[portId] = afdxPacket

def __get_processed_packet(portId):
    global PROCESSED_PORTS
    return PROCESSED_PORTS[portId]

def WRITE(afdxPortId, payload, payloadLength):
    pass

def READ_Sampling(samplingPortId):
    pass

def READ_Queuing(queuingPortId):
    packet = __get_processed_packet(queuingPortId)
    if packet != None:
        payload = packet.getPayload()
        if payload != None:
            return payload, len(payload)
    return (None, 0)

def GET_InputVl(vlId):
    return __get_vl(vlId, ICD_INPUT_VL)

def GET_OutputVl(vlId):
    return __get_vl(vlId, ICD_OUTPUT_VL)
