from com.afdxsuite.scripts import Script
from com.afdxsuite.core.network import NETWORK_AB
from com.afdxsuite.config.parsers import ICD_INPUT_VL

class Script013(Script):
    application = None
    def __init__(self, application):
        self.application = application
        super(Script013, self).__init__("ITR-ES-013", has_sequences = True)
        self.input_ports = self.getPorts({'network_select' : NETWORK_AB},
                                         ICD_INPUT_VL)

    def sequence1(self):
        pass

    def sequence2(self):
        pass

    def sequence3(self):
        pass

    def sequence4(self):
        pass

    def sequence5(self):
        pass

    def run(self):
        self.sequence1()