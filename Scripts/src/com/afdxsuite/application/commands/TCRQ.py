from com.afdxsuite.application.commands import Command
from com.afdxsuite.application.utilities import i2h

class TCRQ(Command):
    __application = None
    
    def __init__(self):
        super(TCRQ, self).__init__()

    def buildCommand(self, loop_count = 1):
        command = "%(tesn)sTCRQ%(count)s" % \
        {'tesn' : i2h("%04X" % self.getTESN()),
         'count' : i2h("%04X" % loop_count)}
        return command.decode('string_escape')