from com.afdxsuite.application.properties import get
from com.afdxsuite.core.network.airscapy import sniff
from com.afdxsuite.core.network.receiver.Listeners import Listeners

import threading
from com.afdxsuite.core.network import NETWORK_A, NETWORK_B
from com.afdxsuite.core.network.scapy import Ether, IP

class ThreadExit(Exception):
    def __init__(self):
        print "Thread terminated"
        super(Exception, self).__init__()

class ReceiverThread(threading.Thread):

    __stop = False
    __network = None

    def __init__(self, network):
        self.__network = network
        self.__iface   = get("NETWORK_INTERFACE_" + network)
        self.listeners = Listeners()
        super(ReceiverThread, self).__init__()

    def callback(self, packet):
        if self.__stop:
            raise ThreadExit()

        self.listeners.notifyListeners(packet, self.__network)

    def run(self):
        try:
            filter_text = get("RECEIVER_NETWORK_FILTER_" + self.__network)

            while True:
                sniff(iface = self.__iface, prn = self.callback,
                      filter = filter_text,
                      store = 0, timeout = 10)

                if self.__stop:
                    break
        except ThreadExit: pass
        except Exception, ex:
            print 'Failed', str(ex)

    def kill(self):
        self.__stop = True


class Receiver(object):

    __network_A = None
    __network_B = None
    
    def __init__(self, network):
        
        if NETWORK_A in network:
            self.__network_A = ReceiverThread(NETWORK_A)

        if NETWORK_B in network:
            self.__network_B = ReceiverThread(NETWORK_B)

    def start(self):
        if self.__network_A != None:
            self.__network_A.start()
        if self.__network_B != None:
            self.__network_B.start()

    def stop(self):
        if self.__network_A != None:
            self.__network_A.kill()
        if self.__network_B != None:
            self.__network_B.kill()

    def reset(self):
        pass