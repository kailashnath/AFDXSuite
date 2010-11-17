from com.afdxsuite.application.utilities import h2i
from com.afdxsuite.core.network.receiver.Receiver import Receiver

class Command(object):

    def getTESN(self):
        return testequipment_sequencer.getTESN()

    def send(self):
        raise Exception("Method not implemented")

class SequenceHandler(object):
    __seq_no = -1

    def __init__(self):
        pass

    def getTESN(self):
        sn = self.__seq_no
        if sn == 65535:
            sn = 0
        else:
            sn += 1

        self.__seq_no = sn
        return sn

    def reset(self):
        self.__seq_no = -1

testequipment_sequencer = SequenceHandler()
