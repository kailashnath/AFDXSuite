from com.afdxsuite.application.TestResponder import Command,\
    testresponder_sequencer
from com.afdxsuite.application.TestResponder.utils import i2h
from com.afdxsuite.config.Factory import READ, WRITE, GET_Port_Input

import time
from com.afdxsuite.config.parsers.icdparser import PORT_SAMPLING

class RRPC(Command):
    __application = None
    __parent_portId = None
    __response = "OK   "
    tesn_index = 0
    comport_index = 6

    def __init__(self, payload, application = None, 
                 parent_portId = None, **kwargs):
        super(RRPC, self).__init__(payload)
        self.__application = application
        self.__parent_portId = parent_portId

    def execute(self):
        port_data = READ(self.getComport())

        if port_data == None:
            self.__response = "ERR  "
            return

        port = GET_Port_Input(self.getComport())

        if port.port_characteristic == PORT_SAMPLING:
            timestamp = i2h(str((int)(time.time()))[-4:])
        else:
            timestamp = ""
        if port_data != None:
            response = "%(trsn)s%(tesn)sRRPC%(comport)s%(timestamp)s%(data)s" %\
            {'trsn' : i2h("%04X" % testresponder_sequencer.getTRSN()),
             'tesn' : i2h("%04X" % self.getTESN()),
             'comport' : i2h(self.getComport()),
             'timestamp' : timestamp,
             'data' : port_data}
            port = WRITE(self.__parent_portId, response.decode('string_escape'))
            self.__application.transmit(port)

    def getResponse(self):
        response = "%(trsn)s%(tesn)s%(response)sRRPC%(comport)s" % \
        {'trsn' : i2h("%04X" % testresponder_sequencer.getTRSN()),
         'tesn' : i2h("%04X" % self.getTESN()),
         'response' : self.__response,
         'comport' : i2h(self.getComport())}

        return response.decode('string_escape')
