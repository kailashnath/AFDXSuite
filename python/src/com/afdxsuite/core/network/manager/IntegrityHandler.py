from com.afdxsuite.core.network.manager.RedundancyHandler import RedundancyHandler
from com.afdxsuite.models.AFDXPacket import AFDXPacket
from com.afdxsuite.logging import afdxLogger

class IntegrityHandler(object):
    __redundancy_handler = None

    def __init__(self):
        pass

    def registerRedundancyHandler(self, handler):
        if isinstance(handler, RedundancyHandler):
            self.__redundancy_handler = handler

    def __doIntegrityCheck(self):
        return True

    def doCheck(self):

        if not self.__doIntegrityCheck():
            afdxLogger.error("The packet failed integrity check")
            return

        afdxLogger.info("The packet has passed the integrity check")

        if(self.__redundancy_handler == None):
            self.__redundancy_handler.doCheck()

    def notify(self, packet):
        if(isinstance(packet, AFDXPacket)):
            self.doCheck()