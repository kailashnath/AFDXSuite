from com.afdxsuite.core.network.receiver.Listeners import IListener
from com.afdxsuite.models.AFDXPacket import AFDXPacket
from com.afdxsuite.logging import afdxLogger
from com.afdxsuite.config import Factory
from com.afdxsuite.core.network.scapy import UDP, Raw, IP
from com.afdxsuite.core.network.manager.PacketChecker import PacketChecker
from com.afdxsuite.core.network import NETWORK_A
from com.afdxsuite.core.network.hooks import *

import traceback, sys
from com.afdxsuite.application.properties import get

class AFDXListener(IListener):

    __integrity_handler     = None
    __redundancy_handler    = None
    __fragmentation_handler = None
    __application           = None
    __packet                = None
    __network               = None
    __hooks                 = None

    def __init__(self, network):
        self._integrity_check_result  = False
        self._redundancy_check_result = False
        self.__network = network
        self.__hooks = eval(get("HOOKS"))
        if self.__hooks == None or type(self.__hooks) != dict:
            self.__hooks = dict()
        else:
            for key in self.__hooks.keys():
                target = self.__hooks[key]
                self.__hooks[key] = target

    def __check(self):
        if self.__packet != None:
            checker = PacketChecker(self.__packet)
            checker.runChecks()
            return checker.isPassed()
        print 'Basic packet checking failed for packet with ip id', \
        self.__packet[IP].id
        return False

    def getNetworkId(self):
        return self.__network

    def notify(self, afdxPacket):
        self.__packet = AFDXPacket(afdxPacket)
        conf = self.__packet.conf_vl

        try:

            if self.__packet != None:

                # removing the condition "conf.ic_active ==  True" and 
                # "conf.rma == True" as for a fragmented packet the conf 
                # will be None as AFDXPacket class cannot find UDP layer
                # in a fragmented packet
                if  self.__packet != None:
                    self.__notifyIntegrityHandler()
                else:
                    return

                if self._integrity_check_result:
                    self.__notifyRedundancyHandler()
                else:
                    return

                if self._integrity_check_result and \
                self._redundancy_check_result:
                    self.__notifyFragmentationHandler()
                    # packet will be made either None or value depending upon
                    # the return value from the Fragmentation handler
                    if self.__packet == None:
                        return
                    else:
                        self.__packet = AFDXPacket(self.__packet)
                        conf = self.__packet.conf_vl

                    if conf == None or not self.__check():
                        return

                    # after both successful the system should go forward
                    Factory.put_processed_packet(self.__packet)
                    for port in self.__hooks.keys():
                        if port == self.__packet[UDP].dport:
                            self.__hooks[port](self.__application, 
                                               self.__packet)
                            return
                    self.__application.notify(conf.RX_AFDX_port_id)
        except Exception, ex:
            print "--------------", str(ex)
            traceback.print_exc(file = sys.stdout)

    def registerIntegrityHandler(self, handler):
        self.__integrity_handler = handler

    def registerRedundancyHandler(self, handler):
        self.__redundancy_handler = handler

    def registerFragmentationHandler(self, handler):
        self.__fragmentation_handler = handler

    def registerApplication(self, application):
        self.__application = application

    def __notifyIntegrityHandler(self):
        if(self.__integrity_handler != None):
            self.__integrity_handler.doCheck(self.__packet)
            self._integrity_check_result = self.__integrity_handler.getResult()
        else:
            afdxLogger.info("This vl id doesn't support integrity checking")
            self._integrity_check_result = True

    def __notifyRedundancyHandler(self):
        if (self.__redundancy_handler != None):
            self.__redundancy_handler.doCheck(self.__packet)
            self._redundancy_check_result = \
                        self.__redundancy_handler.getResult()
        else:
            afdxLogger.info("This vl id doesn't support redundancy checking")
            self._redundancy_check_result = True

    def __notifyFragmentationHandler(self):
        if (self.__fragmentation_handler != None):
            self.__fragmentation_handler.putPacket(self.__packet)
            self.__packet = self.__fragmentation_handler.getPacket()
