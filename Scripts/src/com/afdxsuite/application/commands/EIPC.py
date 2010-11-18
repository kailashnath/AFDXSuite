from com.afdxsuite.application.commands import Command
from com.afdxsuite.application.utilities import i2h

class EIPC(Command):
    __application = None
    port = None
    command_size = 13
    def __init__(self, application, port):
        self.__application = application
        self.port = port
        super(EIPC, self).__init__()

    def buildCommand(self, command = 'SEND', messagetype = 'S', message = ""):
        command = "%(tesn)sEIPC%(comport)s%(command)s"\
                    "%(messagetype)s%(message)s" % \
                    {'tesn' : i2h("%04X" % self.getTESN()),
                     'comport' : i2h("%04X" % self.port.tx_AFDX_port_id),
                     'command' : command,
                     'messagetype' : messagetype,
                     'message' : message}
        return command.decode('string_escape')