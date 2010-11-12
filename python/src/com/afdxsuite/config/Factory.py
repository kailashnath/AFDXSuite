from com.afdxsuite.config.parsers import ICD_INPUT_VL, ICD_OUTPUT_VL
from com.afdxsuite.config.parsers.icdparser import CONFIG_ENTRIES

def __get_vl(vlId, type):

    entries = CONFIG_ENTRIES[type]

    if not isinstance(vlId, basestring):
        vlId = str(vlId)

    for entry in entries:
        if entry.RX_AFDX_port_id == vlId:
            return entry

def WRITE(afdxPortId, payload, payloadLength):
    pass

def READ_Sampling(samplingPortId):
    pass

def READ_Queuing(queuingPortId):
    pass

def GET_InputVl(vlId):
    return __get_vl(vlId, ICD_INPUT_VL)

def GET_OutputVl(vlId):
    return __get_vl(vlId, ICD_OUTPUT_VL)
