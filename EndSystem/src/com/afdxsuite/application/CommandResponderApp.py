from com.afdxsuite.config.Factory import READ_Queuing
from com.afdxsuite.application.AFDXListener import AFDXListener
from com.afdxsuite.core.network.manager.IntegrityHandler import IntegrityHandler
from com.afdxsuite.core.network.manager.FragmentationHandler import FragmentationHandler
from com.afdxsuite.core.network.manager.RedundancyHandler import RedundancyHandler
from com.afdxsuite.core.network import NETWORK_AB, NETWORK_A, NETWORK_B
from com.afdxsuite.core.network.receiver.Listeners import Listeners

class CommandResponderApp(object):
    __receiver    = None
    __transmitter = None
    __listener    = None
    __network     = None

    def __init__(self, transmitter, receiver_class,
                 listener_class, network):
        self.__transmitter = transmitter()
        self.__receiver    = receiver_class(network)
        self.__listener    = listener_class
        self.__network     = network
        self.listeners     = list()
        self.__wire()

    def __wire(self):
        if self.__listener != None:
            fragmentation_handler = FragmentationHandler()
            redundancy_handler    = RedundancyHandler()

            if NETWORK_A in self.__network:
                self.listeners.append(self.__listener(network = NETWORK_A))
            if NETWORK_B in self.__network:
                self.listeners.append(self.__listener(network = NETWORK_B))

            for listener in self.listeners:
                listener.registerApplication(self)
                listener.registerIntegrityHandler(IntegrityHandler())
                listener.registerFragmentationHandler(fragmentation_handler)
                listener.registerRedundancyHandler(redundancy_handler)
                Listeners.registerListener(listener, listener.getNetworkId())

    def activate(self):
        self.__receiver.start()

    def deactivate(self):
        if hasattr(self, 'activeInstance'):
            print 'The application will stop soon'
            self.activeInstance.stop()

    def notify(self, portId):
        payload, payload_len = READ_Queuing(portId)
        print payload_len
        self.__transmitter.write(portId, payload)
        self.__transmitter.transmit(self.__network)