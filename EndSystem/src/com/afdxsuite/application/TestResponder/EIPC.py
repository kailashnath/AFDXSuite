from com.afdxsuite.application.TestResponder import Command,\
    testresponder_sequencer, reaction_queue
from com.afdxsuite.application.TestResponder.utils import i2h
from com.afdxsuite.config.Factory import WRITE

EIPC_HOLD = 'HOLD'
EIPC_SEND = 'SEND'

class EIPC(Command):

    tesn_index = 0
    comport_index = 6
    __sendorhold = None
    __messageType = None
    __text = None
    __response = 'OK   '
    __application = None

    def __init__(self, payload, application = None, **kwargs):
        super(EIPC, self).__init__(payload)
        self.__application = application
        self.__sendorhold = payload[8 : 12]
        self.__messageType = payload[12]
        self.__text = payload[13:]

    def __sendOnPort(self):
        try:
            portId = self.getComport()
            response = "%(tesn)s%(trsn)sEIPC%(comport)s%(type)s%(text)s" % \
            {'tesn' : i2h("%04X" % self.getTESN()),
             'trsn' : i2h("%04X" % testresponder_sequencer.getTRSN()),
             'comport' : i2h(self.getComport()),
             'type' : self.__messageType,
             'text' : self.__text}
            port = WRITE(portId, response.decode('string_escape'))
            self.__application.transmit(port)
            return True
        except:
            return False

    def execute(self):
        action_status = False
        if self.__sendorhold == EIPC_HOLD:
            action_status = reaction_queue.push(self)
        else:
            action_status = self.__sendOnPort()
        if not action_status:
            self.__response = 'ERR  '

    def tcrq_send(self):
        self.__sendOnPort()

    def getResponse(self):
        response = "%(trsn)s%(tesn)s%(response)sEIPC%(com_port)s" % \
        {'trsn' : i2h("%04X" % testresponder_sequencer.getTRSN()),
         'tesn' : i2h("%04X" % self.getTESN()),
         'com_port' : i2h(self.getComport()),
         'response' : self.__response}
        return response.decode('string_escape')
