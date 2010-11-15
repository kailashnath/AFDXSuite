from com.afdxsuite.core.network import NETWORK_A, NETWORK_AB, NETWORK_B
from com.afdxsuite.application.CommandResponderApp import CommandResponderApp
from com.afdxsuite.core.network.receiver.Receiver import Receiver

import time
from com.afdxsuite.application.AFDXListener import AFDXListener
from com.afdxsuite.core.network.transmitter.Transmitter import Transmitter

if __name__ == '__main__':

    application = CommandResponderApp(Transmitter, receiver_class = Receiver,
                                      listener_class = AFDXListener, 
                                      network = NETWORK_AB)
    application.activate()
    #application.deactivate()11