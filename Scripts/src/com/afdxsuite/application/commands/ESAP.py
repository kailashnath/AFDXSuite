from com.afdxsuite.application.commands import Command
from com.afdxsuite.application.utilities import i2h, iptoHexarray

class ESAP(Command):
    __application = None
    port = None
    command_size = 19

    def __init__(self, application, port):
        self.__application = application
        self.port = port
        super(ESAP, self).__init__()

    def buildCommand(self, command = 'SEND', messagetype = 'S',  message = ""):
        port = self.port
        command = "%(tesn)sESAP%(sapsrcport)s%(command)s%(commandtype)s"\
                        "%(message)s%(teip)s%(udpdst)s" % \
                        {'tesn' : i2h("%04X" %self.getTESN()),
                         'sapsrcport' : i2h("%04X" % port.udp_src),
                         'command' : command,
                         'commandtype' : messagetype,
                         'message' : message,
                         'teip' : iptoHexarray(port.ip_dst),
                         'udpdst' : i2h("%04X" % port.udp_dst)}
        return command.decode('string_escape')