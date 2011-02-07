from com.afdxsuite.core.network.receiver.Receiver import IReceiver, Receiver
from com.afdxsuite.core.network.scapy import conf
from com.afdxsuite.config.parsers.icdparser import PORT_SAMPLING
from com.afdxsuite.core.network import NETWORK_A
from com.afdxsuite.logger import general_logger

import time

# MIB CONSTANTS
MIB_MAC_GROUP         = "afdxMAC"
MIB_EQUIPMENT_GROUP   = "afdxEquipment"
MIB_IP_GROUP          = "afdxIP"
MIB_UDP_GROUP         = "afdxUDP"
MIB_ES_FAILURE_GROUP  = "afdxESFailure"

class ResponsePoller(IReceiver):
    
    def __init__(self):
        self.command = None
        self.status = False
    
    def pollForCommand(self, command):
        if type(command) not in (list, tuple):
            command = [command]
        self.command = command

    def notify(self, packet):
        try:
            if self.command != None:
                for cmd in self.command:
                    if cmd in str(packet).encode('string_escape'):
                        self.command = None
                        self.status = True
        except Exception, ex:
            print ex

command_poller = ResponsePoller()
Receiver.register(command_poller, NETWORK_A)
general_logger.info("Command poller initialized.......")

def h2i(value):
    if type(value) == str:
        return int(value.encode('hex'), 16)

def i2h(value):

    if type(value) == int:
        if value < 255:
            return "\\x%02X" % value
        else:
            val = "%04X" % value
            return "\\x%s\\x%s" % (val[0:2], val[2:4])
    else:
        value = "%04s" % value
        return "\\x%s\\x%s" % (value[0:2], value[2:4])

def hexarrayTointarray(hex_array):
    response = list()
    for hexval in hex_array:
        response.append(h2i(hexval))
    return response

def iptoHexarray(ip_address):
    ip_vals = ip_address.split('.')
    ip_vals = map(lambda x : int(x), ip_vals)
    return "\\x%02X\\x%02X\\x%02X\\x%02X" % (ip_vals[0], ip_vals[1], \
                                             ip_vals[2], ip_vals[3])

def pollForResponse(command, timeout = 2, logger = None):
    time.sleep(2)
    return True

    # the below code is no more valid as we are not validating against
    # any received packets. Hence commenting out the code
    """
    global command_poller

    if command_poller == None:
        command_poller = ResponsePoller()
        Receiver.register(command_poller, 'A')

    command_poller.status = False
    command_poller.pollForCommand(command)
    while True:

        if command_poller.status:
            return True
        if timeout == 0:
            return False
        timeout -= 1
        time.sleep(1)
    """

def buildBigMessage(port, message = "", offset_size = 0):
    mfs = port.max_frame_size

    new_size = int(mfs) - offset_size - len(message)

    if port.port_characteristic != PORT_SAMPLING:
        new_size += 100

    if new_size > int(port.buffer_size):
        new_size = int(port.buffer_size) - offset_size - len(message)

    message = message + "*" * new_size

    return message

def buildShortMessage(port, message = "", offset_size = 0):
    # short message is something that is less than max frame size as well as
    # less than buffer size
    acceptable_size = int(port.max_frame_size) \
        if int(port.max_frame_size) < int(port.buffer_size) \
        else int(port.buffer_size)
    mfs = int(port.max_frame_size)

    new_size = acceptable_size - (offset_size + len(message))
    if new_size < 0:
        return message[:(mfs - offset_size)]
    else:
        return message[:new_size]

def buildMessage(port, size, message = ""):

    acceptable_size = size \
        if size < int(port.buffer_size) else int(port.buffer_size)

    if size > acceptable_size:
        size = acceptable_size

    if len(message) > size:
        new_message = message[:size]
    else:
        new_message = message + "*" * (size - len(message))
    return new_message

def buildStaticMessage(size, message = ""):
    newsize = size - len(message)
    message = message + "*" * newsize
    return message

def buildFragmentedMessage(port, noofFragments, message = ""):
    msg_size = len(message)
    mfs = int(port.max_frame_size)
    if mfs > 1471:
        mfs = 1471
    new_size = (mfs * noofFragments) - msg_size

    if new_size > port.buffer_size:
        new_size = port.buffer_size

    return message + "*" * (new_size - 8)



################################################################################
def getAFDXEquipmentGroup(extra_id = 0):
    """
        Returns the oid list for AFDX Equipment Group
    """
    return getMIBGroup(MIB_EQUIPMENT_GROUP, extra_id)

################################################################################################################
def getAFDXESFailureGroup(extra_id = 0):
    """
        Returns the oid list for AFDX ES Failure Group
    """
    return getMIBGroup(MIB_ES_FAILURE_GROUP, extra_id)

################################################################################################################
def getAFDXIPGroup(extra_id = 0):
    """
        Returns the oid list for AFDX IP Group
    """
    return getMIBGroup(MIB_IP_GROUP, extra_id)

################################################################################################################
def getAFDXMACGroup(extra_id = 1):
    """
        Returns the oid list for AFDX Mac Group
    """
    return getMIBGroup(MIB_MAC_GROUP, extra_id)

################################################################################################################
def getAFDXUDPGroup(extra_id = 0):
    """
        Returns the oid list for AFDX UDP Group
    """
    return getMIBGroup(MIB_UDP_GROUP, extra_id)

################################################################################################################
def getMIBGroup(group_name, extra_id = None):
    """
        Returns an oid list from the leafs of the requested group
    """
    oid_lst = []
    for key in conf.mib.keys():
        if group_name in key and len(key) > len(group_name) and "Group" not in key:
            oid_value = getMIBOID(key, extra_id)
            oid_lst.append(oid_value)

    oid_lst.sort()
    return oid_lst

################################################################################################################
def getMIBOID(oid_name, extra_id = 0):
    """
        Returns the OID for the giving oid name
    """
    oid_value = conf.mib[oid_name]
    if extra_id != None:
        oid_value += "." + str(extra_id)

    return oid_value

def getMIBOIDBySize(size):

    oids = []

    while len(oids) < size:
        for key in conf.mib.keys():
            suffix = ".0"
            oid = conf.mib[key]

            if key in ['afdxEquipment', 'afdxMAC', 'afdxRedundancy', 'afdxIP',
                   'afdxICMP', 'afdxUDP', 'afdxTCP', 'afdxESFailure',
                   'afdxMACTable', 'afdxMACEntry', 'afdxRedundancyErrorTable',
                   'afdxRedundancyStatsTable', 'afdxRedundancyErrorEntry',
                   'afdxRedundancyStatsEntry', 'afdxEndSystem', 'airbus',
                   'afdx', 'afdxEndSystemMIB', 'afdxESConformance',
                   'afdxESGroups', 'afdxESCompliances']:
                continue

            if not 'enterprises' in oid:
                continue

            if str(key).find('afdxRedundancy') > -1 or \
            str(key).find('afdxMAC') > -1 or str(key).find('afdxTCP') > -1 or \
            str(key).find('afdxESFailure') > -1:
                #suffix = ".1"
                continue

            oid += suffix

            if len(oids) == size:
                return oids
            oids.append(oid)
    return oids
