from com.afdxsuite.application.commands import Command
from com.afdxsuite.application.utilities import i2h

class ERPQ(Command):
    port = None

    def __init__(self, port):
        self.port = port
        super(ERPQ, self).__init__()

    def buildCommand(self):
        command = "%(tesn)sERPQ%(port)s" % \
        {'tesn' : i2h("%04X" % self.getTESN()),
         'port' : i2h("%04X" % self.port.RX_AFDX_port_id)
         }
        return command.decode('string_escape')