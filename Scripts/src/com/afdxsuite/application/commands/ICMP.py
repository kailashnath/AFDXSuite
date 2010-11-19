from com.afdxsuite.application.commands import Command

class ICMP(Command):
    port = None

    def __init__(self, port):
        self.port = port
        super(ICMP, self).__init__()