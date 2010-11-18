from com.afdxsuite.core.network.receiver.Receiver import IReceiver, Receiver

import time
from com.afdxsuite.core.network import NETWORK_AB
from com.afdxsuite.core.network.scapy import IP, UDP, Raw
from com.afdxsuite.config.parsers.icdparser import PORT_QUEUING, PORT_SAMPLING

command_poller = None

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

def pollForResponse(command, timeout = 5):
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
