
class SequenceHandler(object):
    
    def __init__(self):
        self.__current_sn = {}
        self.__ipid = 1

    def next(self, vlId):
        sn = self.__current_sn[vlId] if self.__current_sn.has_key(vlId) else -1

        if sn > 255:
            sn = 1
        else:
            sn += 1

        self.__current_sn[vlId] = sn
        return sn

    def nextIpId(self):
        sn = self.__ipid
        if self.__ipid == 65535:
            sn = 1
        else:
            sn += 1
        self.__ipid = sn
        return self.__ipid
