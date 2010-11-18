from com.afdxsuite.application.commands import Command
from com.afdxsuite.application.utilities import i2h

class RSET(Command):
    __application = None

    def __init__(self):
        super(RSET, self).__init__()

    def buildCommand(self):
        command = "%(tesn)sRSET" % {'tesn' : i2h("%04X" % self.getTESN())}

        return command.decode('string_escape')