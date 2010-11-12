from com.afdxsuite.core.network.receiver import NETWORK_A, NETWORK_B
from com.afdxsuite.application.properties import get
from com.afdxsuite.core.network.airscapy import sniff
from com.afdxsuite.core.network.receiver.Listeners import Listeners

import threading
from com.afdxsuite.core.network.scapy import Ether

class ThreadExit(Exception):
    def __init__(self):
        print "Thread terminated"
        super(Exception, self).__init__()

class ReceiverThread(threading.Thread):

    __stop = False

    def __init__(self, iface):
        self.__iface = iface
        self.listeners = Listeners()
        super(ReceiverThread, self).__init__()

    def callback(self, packet):
        if self.__stop:
            raise ThreadExit()

        self.listeners.notifyListeners(packet)

    def run(self):
        try:
            sniff(iface = self.__iface, prn = self.callback,
                  filter = get("RECEIVER_NETWORK_FILTER"), store = 0)
        except ThreadExit:
            print 'Receiver stopped'
            pass
        except Exception, ex:
            print ex

    def kill(self):
        self.__stop = True


class Receiver(object):

    __network_A = None
    __network_B = None
    
    def __init__(self, network):
        
        if NETWORK_A in network:
            self.__network_A = ReceiverThread(get("NETWORK_INTERFACE_A"))

        if NETWORK_B in network:
            self.__network_B = ReceiverThread(get("NETWORK_INTERFACE_B"))

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
