from com.afdxsuite.logging import afdxLogger
from com.afdxsuite.core.network.receiver.Receiver import Receiver
from com.afdxsuite.core.network.receiver import NETWORK_A
from com.afdxsuite.core.network.receiver.Listeners import IListener, Listeners

import time

if __name__ == '__main__':
    dummy_listener = IListener()
    receiver = Receiver(NETWORK_A)
    receiver.start()
    Listeners.registerListener(dummy_listener)

