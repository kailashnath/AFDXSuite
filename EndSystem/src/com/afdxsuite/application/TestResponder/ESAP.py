from com.afdxsuite.application.TestResponder import Command, reaction_queue,\
    testresponder_sequencer
from com.afdxsuite.application.TestResponder.utils import i2h,\
    hexarrayTointarray, h2i
from com.afdxsuite.config.Factory import WRITE_Sap

ESAP_HOLD = 'HOLD'
ESAP_SEND = 'SEND'

class ESAP(Command):

    tesn_index = 0
    sapport_index = 6 
    __sendorhold = None
    __messageType = None
    __text = None
    __response = 'OK   '
    __application = None
    __sapsrcPort = None
    __teipaddress = None
    __udpdstport = None
    __application = None

    def __init__(self, payload, application = None, **kwargs):
        super(ESAP, self).__init__(payload)
        self.__application = application
        self.__sendorhold = payload[8 : 12]
        self.__messageType = payload[12]
        self.__text = payload[13 : -6]
        self.__sapsrcPort = self.getSapSrcport()
        self.__udpdstport = h2i(payload[-2:])
        print payload[-6:-2], hexarrayTointarray(payload[-6:-2])
        self.__teipaddress = reduce(lambda x, y : "%s.%s" % (x, y), \
                                    hexarrayTointarray(payload[-6:-2]))

    def __sendOnPort(self):
        try:
            response = "%(trsn)s%(tesn)sESAP%(sapsrcport)s%(type)s%(text)s" % \
            {'trsn' : i2h("%04X" % testresponder_sequencer.getTRSN()),
             'tesn' : i2h("%04X" % self.getTESN()),
             'sapsrcport' : i2h(self.getSapSrcport()),
             'type' : self.__messageType,
             'text' : self.__text}
    
            port = WRITE_Sap(self.getSapSrcport(), response.decode('string_escape'),
                             self.__teipaddress, self.__udpdstport)
            self.__application.transmit(port)
            return True
        except Exception, ex:
            print 'Exception at esap', str(ex)
            return False
        

    def execute(self):
        if self.__sendorhold == ESAP_HOLD:
            reaction_queue.push(self)
        else:
            if not self.__sendOnPort():
                self.__response = "ERR  "

    def tcrq_send(self):
        self.__sendOnPort()

    def getResponse(self):
        response = "%(trsn)s%(tesn)s%(response)sESAP%(sapsrcport)s" % \
        {'trsn' : i2h("%04X" % testresponder_sequencer.getTRSN()),
         'tesn' : i2h("%04X" % self.getTESN()),
         'response' : self.__response,
         'sapsrcport' : i2h(self.getSapSrcport())}
        return response.decode('string_escape')
