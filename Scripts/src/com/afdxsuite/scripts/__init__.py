from com.afdxsuite.core.network.receiver.Receiver import IReceiver, Receiver
from com.afdxsuite.core.network.scapy import PcapWriter
from com.afdxsuite.application import CAPTURES_PARENT_DIRECTORY,\
    LOGGER_PARENT_DIRECTORY
from com.afdxsuite.logger import Logger, general_logger
from com.afdxsuite.config import Factory
from com.afdxsuite.application.commands.RSET import RSET
from com.afdxsuite.application.utilities import pollForResponse
from com.afdxsuite.application.properties import get

import os
from com.afdxsuite.core.network import NETWORK_AB

class ScriptReceiver(IReceiver):
    __writer = None
    __filter = None
    __scriptName = None

    def __init__(self, scriptName):
        self.__scriptName = scriptName

    def start(self, seqno = 0):
        filename = self.__scriptName
        if seqno > 0:
            filename = self.__scriptName + "_SEQ" + str(seqno) + ".cap"
        if self.__writer != None:
            self.stop()
        self.__writer = PcapWriter(CAPTURES_PARENT_DIRECTORY + "/" + \
                                   filename)

    def notify(self, packet):
        if self.__filter != None:
            if not self.__filter(packet):
                return

        self.__writer.write(packet)

    def setFilter(self, filterfunc):
        self.__filter = filterfunc

    def stop(self):
        if self.__writer != None:
            self.__writer.close()
            self.__writer = None

class Script(object):
    __receiver = None
    __scriptName = None
    logger = general_logger
    network  = 'A'

    def __init__(self, name, has_sequences = False):
        self.logger = \
        Logger(LOGGER_PARENT_DIRECTORY, logger_name = name).script_logger
        self.logger.info("Intialising the script " + name)
        self.__receiver = ScriptReceiver(name)

        if not has_sequences:
            self.__receiver.start()

        self.__scriptName = name
        Receiver.register(self.__receiver, NETWORK_AB)

    def captureForSequence(self, seqNo):
        self.__receiver.start(seqNo)

    def getPorts(self, filter, port_type):
        result_ports = []
        ports = Factory.GET_Ports(None, port_type)
    
        for port in ports:
            if type(filter) == dict:
                add = True
                for key in filter.keys():
                    if hasattr(port, key):
                        lhs_val = getattr(port, key)
                        rhs_val = filter[key]
                        if type(rhs_val) in (list, tuple):
                            condition = lhs_val in rhs_val
                        else:
                            condition = lhs_val == rhs_val
                        if not condition:
                            add = False
                            break
                    else:
                        add = False
                        break
                if add:
                    result_ports.append(port)
            else:
                if filter(port):
                    result_ports.append(port)
    
        return result_ports

    def remove_common_ports(self, ports):
        filtered_ports = []
        for port in ports:
            if hasattr(port, 'udp_src'):
                val = port.udp_src
            elif hasattr(port, 'udp_dst'):
                val = port.udp_dst
            if val in (int(get("TE_UDP")), int(get("TE_SNMP"))):
                continue
            filtered_ports.append(port)
        return filtered_ports

    def send(self, payload, ports):
        if type(ports) != list:
            ports = [ports]

        for port in ports:
            outport = Factory.WRITE(port.RX_AFDX_port_id, payload)
            self.application.transmitter.transmit(outport, self.network)

    def sendRSET(self, poll = True):
        rset = RSET()
        self.send(rset.buildCommand(), Factory.GET_TX_Port())
        if not poll:
            return
        if not pollForResponse('OK'):
            self.logger.error("The ES has not responded to RSET")

    def stop(self):
        self.logger.info("Stopping the script " + self.__scriptName)
        self.__receiver.stop()
