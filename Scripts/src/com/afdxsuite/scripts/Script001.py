from com.afdxsuite.application.commands.RSET import RSET
from com.afdxsuite.scripts import Script
from com.afdxsuite.config import Factory
from com.afdxsuite.config.parsers import ICD_INPUT_VL
from com.afdxsuite.application.utilities import pollForResponse

class Script001(Script):
    application = None
    network = 'A'

    def __init__(self, application):
        super(Script001, self).__init__("ITR-ES-001", application.network)
        self.network = application.network
        self.ports = Factory.GET_Ports(self.ports_filter, ICD_INPUT_VL)
        self.application = application

    def ports_filter(self, port):
        if port.vl_id == 1 and port.network_id == self.network:
            return True
        return False

    def run(self):
        rset = RSET(self.application, None)
        self.send(rset.buildCommand(), Factory.GET_TX_Port())
        if not pollForResponse('OK'):
            print 'no response found'
        else:
            print 'response found'

    def stop(self):
        super(Script001, self).stop()
