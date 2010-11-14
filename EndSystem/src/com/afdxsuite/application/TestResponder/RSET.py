from com.afdxsuite.application.TestResponder import reaction_queue,\
    testresponder_sequencer, Command
from com.afdxsuite.application.TestResponder.utils import i2h

class RSET(Command):
    __command  = None
    tesn_index = 0

    def __init__(self, command, **kwargs):

        super(RSET, self).__init__(command)

    def execute(self):
        reaction_queue.reset()
        testresponder_sequencer.reset()
        self.__command = 'OK\0\0\0'

    def getResponse(self):
        response = "%(trsn)s%(tesn)sOK\0\0\0KAILASH" % \
        {'trsn' : i2h("%04X" % testresponder_sequencer.getTRSN()),
         'tesn' : i2h("%04X" % self.getTESN())}

        return response.decode('string_escape')
