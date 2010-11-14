from com.afdxsuite.application.TestResponder import Command,\
    testresponder_sequencer
from com.afdxsuite.config.Factory import WRITE
from com.afdxsuite.application.TestResponder.utils import i2h

class ERPQ(Command):
    tesn_index = 0
    comport_index = 6

    def __init__(self, payload, **kwargs):
        super(ERPQ, self).__init__(payload)

    def execute(self):
        WRITE(self.getComport(), None)

    def getResponse(self):
        response = "%(trsn)s%(tesn)sOK   ERPQ%(comport)s" % \
        {'trsn' : i2h("%04X" % testresponder_sequencer.getTRSN()),
         'tesn' : i2h("%04X" % self.getTESN()),
         'comport' : i2h(self.getComport())}

        return response.decode('string_escape')
