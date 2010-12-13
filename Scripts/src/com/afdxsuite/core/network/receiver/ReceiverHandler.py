from com.afdxsuite.application.properties import get
from com.afdxsuite.core.network.airscapy import sniff
from com.afdxsuite.core.network import NETWORK_A, NETWORK_B
from com.afdxsuite.core.network.receiver.Receiver import Receiver
from com.afdxsuite.logger import general_logger

import threading, sys, traceback

class ThreadExit(Exception):
    def __init__(self):
        super(Exception, self).__init__()

class ReceiverThread(threading.Thread):

    __stop = False
    __network = None

    def __init__(self, network):
        self.__network = network
        self.__iface   = get("NETWORK_INTERFACE_" + network)

        super(ReceiverThread, self).__init__()

    def callback(self, packet):
        if self.__stop:
            raise ThreadExit()
        Receiver.notifyHandlers(packet, self.__network)

    def run(self):
        try:
            filter_text = get("RECEIVER_NETWORK_FILTER_" + self.__network)
            while True:
                sniff(iface = self.__iface, prn = self.callback,
                      filter = filter_text, timeout = 10,
                      store = 0)

                if self.__stop:
                    raise ThreadExit()
        except ThreadExit:
            general_logger.info("Thread on network " + self.__network + 
                                " stopped")
        except Exception, ex:
            general_logger.error("Exception occured at receiver for network " +\
                                 self.__network + " : " + str(ex))
            general_logger.info("The application will not listen for packets" +\
                                " coming on network : " + self.__network)
            traceback.print_exc(file=sys.stdout)
            general_logger.error("Crash", exc_info = 1)

    def kill(self):
        self.__stop = True

class ReceiverHandler(object):

    __network_A = None
    __network_B = None

    def __init__(self, network):
        
        if NETWORK_A in network:
            self.__network_A = ReceiverThread(NETWORK_A)
            general_logger.info("Intialising receiver on network A")

        if NETWORK_B in network:
            self.__network_B = ReceiverThread(NETWORK_B)
            general_logger.info("Intialising receiver on network B")

    def start(self):
        if self.__network_A != None:
            general_logger.info("Starting the receiver threads on network A")
            self.__network_A.start()
        if self.__network_B != None:
            general_logger.info("Starting the receiver threads on network B")
            self.__network_B.start()

    def stop(self):
        general_logger.info("Stopping the receiver threads on network. " +\
                            "This may take some time.")
        if self.__network_A != None:
            self.__network_A.kill()
        if self.__network_B != None:
            self.__network_B.kill()

    def reset(self):
        pass
