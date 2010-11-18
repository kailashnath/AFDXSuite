from com.afdxsuite.core.network import NETWORK_A, NETWORK_AB, NETWORK_B, scapy
from com.afdxsuite.application.CommandResponderApp import CommandResponderApp
from com.afdxsuite.core.network.receiver.Receiver import Receiver

import time
from com.afdxsuite.application.AFDXListener import AFDXListener
from com.afdxsuite.core.network.transmitter.Transmitter import Transmitter
from com.afdxsuite.core.network.scapy import load_mib, ConfClass

if __name__ == '__main__':

    application = CommandResponderApp(Transmitter, receiver_class = Receiver,
                                      listener_class = AFDXListener, 
                                      network = NETWORK_A)
    application.activate()
    
    #application.deactivate()11