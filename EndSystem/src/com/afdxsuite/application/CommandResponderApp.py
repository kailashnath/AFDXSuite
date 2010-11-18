from com.afdxsuite.config.Factory import READ_Queuing, WRITE
from com.afdxsuite.core.network.manager.IntegrityHandler import IntegrityHandler
from com.afdxsuite.core.network.manager.FragmentationHandler import FragmentationHandler
from com.afdxsuite.core.network.manager.RedundancyHandler import RedundancyHandler
from com.afdxsuite.core.network import NETWORK_A, NETWORK_B
from com.afdxsuite.core.network.receiver.Listeners import Listeners
from com.afdxsuite.application.handlers import COMMAND_HANDLERS

class CommandResponderApp(object):
    __receiver    = None
    __transmitter = None
    __listener    = None
    __network     = None
    listeners     = list()

    def __init__(self, transmitter, receiver_class,
                 listener_class, network):
        self.__transmitter = transmitter()
        self.__receiver    = receiver_class(network)
        self.__listener    = listener_class
        self.__network     = network
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
        payload = READ_Queuing(portId)
        if payload == None:
            return
        for command_name in COMMAND_HANDLERS.keys():
            if command_name in payload:
                handler = COMMAND_HANDLERS[command_name]
                handler = handler(payload, application = self, 
                                  parent_portId = portId)

                handler.execute()

                response = handler.getResponse()
                port = WRITE(portId, response)
                self.__transmitter.transmit(port, self.__network)

    def transmit(self, port):
        self.__transmitter.transmit(port, self.__network)

    def reset(self):
        self.__transmitter.reset()
        self.__receiver.reset()
        self.__listener.reset()
        for listener in self.listeners:
            listener.reset()
