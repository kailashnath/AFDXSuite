from com.afdxsuite.models.AFDXPacket import AFDXPacket
from com.afdxsuite.core.network import NETWORK_A, NETWORK_B

LISTENERS_DICT = {NETWORK_A : list(), NETWORK_B : list()}

class IListener(object):
    def __init__(self):
        pass

    def notify(self, afdxPacket):
        print AFDXPacket(afdxPacket).conf_vl

class Listeners(object):

    def __init__(self):
        pass

    @staticmethod
    def registerListener(listener, network):

        if isinstance(listener, IListener):
            global LISTENERS_DICT
            LISTENERS_DICT[network].append(listener)

    @staticmethod
    def deregisterListener(listener, network):
        if isinstance(listener, IListener):
            global LISTENERS_DICT
            LISTENERS_DICT[network].remove(listener)

    def notifyListeners(self, packet, network):
        global LISTENERS_DICT
        listeners = LISTENERS_DICT[network]

        for listener in listeners:
            listener.notify(packet)
    