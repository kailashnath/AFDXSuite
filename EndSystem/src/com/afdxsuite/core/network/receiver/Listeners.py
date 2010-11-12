from com.afdxsuite.models.AFDXPacket import AFDXPacket

LISTENERS_LIST = []

class IListener(object):
    def __init__(self):
        pass

    def notify(self, afdxPacket):
        print AFDXPacket(afdxPacket).conf_vl

class Listeners(object):

    def __init__(self):
        pass

    @staticmethod
    def registerListener(listener):
        print 'registering the listener'
        if isinstance(listener, IListener):
            global LISTENERS_LIST
            LISTENERS_LIST.append(listener)

    @staticmethod
    def deregisterListener(listener):
        if isinstance(listener, IListener):
            global LISTENERS_LIST
            LISTENERS_LIST.remove(listener)

    def notifyListeners(self, packet):
        global LISTENERS_LIST
        listeners = LISTENERS_LIST
        for listener in listeners:
            listener.notify(packet)
    