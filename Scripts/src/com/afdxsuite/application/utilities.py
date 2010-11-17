from com.afdxsuite.core.network.receiver.Receiver import IReceiver, Receiver

import time
from com.afdxsuite.core.network import NETWORK_AB
from com.afdxsuite.core.network.scapy import IP, UDP, Raw

command_poller = None

class ResponsePoller(IReceiver):
    
    def __init__(self):
        self.command = None
        self.status = False
    
    def pollForCommand(self, command):
        self.command = command

    def notify(self, packet):
        try:
            if self.command != None:
                if self.command in str(packet).encode('string_escape'):
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

def pollForResponse(command, timeout = 5):
    global command_poller

    if command_poller == None:
        command_poller = ResponsePoller()
        Receiver.register(command_poller, 'A')

    command_poller.pollForCommand(command)
    while True:

        if command_poller.status:
            return True
        if timeout == 0:
            return False
        timeout -= 1
        time.sleep(1)
