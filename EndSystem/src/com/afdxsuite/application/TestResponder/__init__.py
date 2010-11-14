from com.afdxsuite.application.TestResponder.utils import h2i

class Command(object):
    __command = None

    def __init__(self, command):
        self.__command = command

    def getTESN(self):
        # __tesn is the position index for the test equipment sequence number
        sn = self.__command[self.tesn_index : self.tesn_index + 2]
        return int(sn.encode('hex'), 16)

    def getComport(self):
        if hasattr(self, 'comport_index'):
            port = self.__command[self.comport_index : self.comport_index + 2]
            return h2i(port)

    def getSapport(self):
        if hasattr(self, 'sapport_index'):
            port = self.__command[self.comport_index : self.comport_index + 2]
            return h2i(port)

class ReactionQueue(object):
    __queue = list()

    def __init__(self):
        print 'Reaction queue initialised'

    def push(self, value):
        if len(self.__queue) == 8192:
            return False
        self.__queue.append(value)
        return True

    def pop(self):
        return self.__queue.pop(0)

    def reset(self):
        self.__queue = list()

    def transmit(self, count):
        for i in range(0, count):
            print 'Sending contents of reaction queue %d time' % i
            for command in self.__queue:
                command.tcrq_send()
        return True

class SequenceHandler(object):
    __seq_no = -1

    def __init__(self):
        pass

    def getTRSN(self):
        sn = self.__seq_no
        if sn == 65535:
            sn = 0
        else:
            sn += 1

        self.__seq_no = sn
        return sn

    def reset(self):
        self.__seq_no = -1

reaction_queue = ReactionQueue()
testresponder_sequencer = SequenceHandler()
