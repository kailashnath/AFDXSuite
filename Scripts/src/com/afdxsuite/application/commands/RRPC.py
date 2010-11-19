from com.afdxsuite.application.commands import Command
from com.afdxsuite.application.utilities import i2h

class RRPC(Command):
    def __init__(self, port):

        self.port = port
        super(RRPC, self).__init__()

    def buildCommand(self):
        command = "%(tesn)sRRPC%(comport)s" % \
        {'tesn' : i2h("%04X" % self.getTESN()),
         'comport' : i2h("%04X" % self.port.RX_AFDX_port_id)}
        return command.decode('string_escape')