from com.afdxsuite.core.network.receiver.Receiver import IReceiver, Receiver
from com.afdxsuite.core.network.scapy import PcapWriter
from com.afdxsuite.application import CAPTURES_PARENT_DIRECTORY,\
    LOGGER_PARENT_DIRECTORY
import os
from com.afdxsuite.logger import Logger, general_logger
from com.afdxsuite.config import Factory

class ScriptReceiver(IReceiver):
    __writer = None
    __filter = None

    def __init__(self, scriptName):
        self.__writer = PcapWriter(CAPTURES_PARENT_DIRECTORY + "/" + \
                                   scriptName + ".cap")
    def notify(self, packet):
        if self.__filter != None:
            if not self.__filter(packet):
                return

        self.__writer.write(packet)

    def setFilter(self, filterfunc):
        self.__filter = filterfunc

    def stop(self):
        self.__writer.close()

class Script(object):
    __receiver = None
    __scriptName = None
    logger = general_logger

    def __init__(self, name, network):
        self.logger = \
        Logger(LOGGER_PARENT_DIRECTORY, logger_name = name).script_logger
        self.logger.info("Intialising the script " + name)
        #self.__receiver = ScriptReceiver(name)
        self.__scriptName = name
        #Receiver.register(self.__receiver, network)

    def getPorts(self, filter):
        pass

    def send(self, payload, ports):
        if type(ports) != list:
            ports = [ports]

        for port in ports:
            outport = Factory.WRITE(port.RX_AFDX_port_id, payload)
            self.application.transmitter.transmit(outport, self.network)

    def stop(self):
        self.logger.info("Stopping the script " + self.__scriptName)
        #self.__receiver.stop()
