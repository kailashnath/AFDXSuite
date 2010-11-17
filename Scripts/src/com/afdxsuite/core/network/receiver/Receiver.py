from com.afdxsuite.core.network import NETWORK_A, NETWORK_B
from com.afdxsuite.core.network.scapy import UDP, IP

LISTENERS_DICT = {NETWORK_A : list(), NETWORK_B : list()}

class IReceiver(object):

    def notify(self, packet):
        raise Exception("Method not implemented")

class Receiver:

    __receivers = []

    @staticmethod
    def register(receiver, network):
        global LISTENERS_DICT

        if not isinstance(receiver, IReceiver):
            return
        print 'registering', receiver, 'on network', network
        if NETWORK_A in network:
            LISTENERS_DICT[NETWORK_A].append(receiver)
        if NETWORK_B in network:
            LISTENERS_DICT[NETWORK_B].append(receiver)

    @staticmethod
    def deregister(receiver, network):
        global LISTENERS_DICT
        LISTENERS_DICT[network].remove(receiver)

    @staticmethod
    def notifyHandlers(packet, network):
        global LISTENERS_DICT

        listeners = LISTENERS_DICT[network]
        for listener in listeners:
            listener.notify(packet)
