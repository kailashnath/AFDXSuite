from com.afdxsuite.application.TestResponder import Command,\
    testresponder_sequencer, reaction_queue
from com.afdxsuite.application.TestResponder.utils import i2h, h2i

class TCRQ(Command):
    __repeatCount = 0
    tesn_index    = 0

    def __init__(self, payload, **kwargs):
        super(TCRQ, self).__init__(payload)
        self.__repeatCount = h2i(payload[6 : 8])

    def execute(self):
        reaction_queue.transmit(self.__repeatCount)

    def getResponse(self):
        response = "%(trsn)s%(tesn)s%(response)sTCRQ%(repeat)s" % \
        {'trsn' : i2h("%04X" % testresponder_sequencer.getTRSN()),
         'tesn' : i2h("%04X" % self.getTESN()),
         'response' : 'OK   ',
         'repeat' : i2h(self.__repeatCount)}
        return response.decode('string_escape')
