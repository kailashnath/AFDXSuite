from com.afdxsuite.config.Factory import READ_Queuing

class CommandResponderApp(object):
    def __init__(self):
        pass

    def notify(self, portId):
        afdxPacket = READ_Queuing(portId)
        print 'App rx packet', afdxPacket