from com.afdxsuite.scripts import Script
from com.afdxsuite.config.parsers.icdparser import PORT_QUEUING
from com.afdxsuite.config.parsers import ICD_INPUT_VL
from com.afdxsuite.application.utilities import buildShortMessage,\
    pollForResponse
from com.afdxsuite.application.commands.ERPQ import ERPQ
from com.afdxsuite.config import Factory
from com.afdxsuite.core.network import NETWORK_A
from com.afdxsuite.application.commands.RRPC import RRPC
import copy

class Script014(Script):
    application = None
    def __init__(self, application):
        self.application = application
        self.network = NETWORK_A
        super(Script014, self).__init__("ITR-ES-014")
        self.input_ports = self.getPorts({'port_characteristic' : PORT_QUEUING},
                                          ICD_INPUT_VL)
        self.sn_vl = {}
        self.sns = [155, 0, 1, 2, 4, 4, 5, 4, 151, 153, 151, 255, 1, 255, 2,
                    235, 236, 237, 238, 239, 240, 241, 242, 243, 244]

    def sn_func(self, vlId):
        if (not self.sn_vl.has_key(vlId)) or (len(self.sn_vl[vlId]) == 0):
            sns = copy.deepcopy(self.sns)
            sns.reverse()
            self.sn_vl[vlId] = sns
        sn = self.sn_vl[vlId].pop()
        self.logger.info("Sends packet with SN = %d" % sn)
        return sn

    def run(self):
        self.sendRSET()
        for port in self.input_ports:
            message = buildShortMessage(port,
                                        "PortId = %s" % port.RX_AFDX_port_id)
            size = len(self.sns)

            while size > 0:
                outport = Factory.WRITE(port.RX_AFDX_port_id, message)
                setattr(port, 'sn_func', self.sn_func)
                self.application.transmitter.transmit(outport, self.network)
    
                rrpc = RRPC(port)
                self.send(rrpc.buildCommand(), Factory.GET_TX_Port())
                pollForResponse('RRPC')
                size -= 1

        erpq = ERPQ(port)
        self.logger.info("Sending an ERPQ command")
        self.send(erpq.buildCommand(), port)
        pollForResponse('ERPQ')

