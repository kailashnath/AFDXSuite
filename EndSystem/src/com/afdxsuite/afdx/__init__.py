from com.afdxsuite.logging import afdxLogger
from com.afdxsuite.core.network.receiver.Receiver import Receiver
from com.afdxsuite.core.network.receiver.Listeners import IListener, Listeners

import time
from com.afdxsuite.application.AFDXListener import AFDXListener
from com.afdxsuite.core.network.manager.IntegrityHandler import IntegrityHandler
from com.afdxsuite.core.network.manager.RedundancyHandler import RedundancyHandler
from com.afdxsuite.core.network import NETWORK_A
from com.afdxsuite.application.CommandResponderApp import CommandResponderApp
from com.afdxsuite.core.network.manager.FragmentationHandler import FragmentationHandler

if __name__ == '__main__':

    receiver = Receiver(NETWORK_A)
    receiver.start()
    application = CommandResponderApp()

    listener = AFDXListener()
    listener.registerApplication(application)
    listener.registerIntegrityHandler(IntegrityHandler())
    listener.registerRedundancyHandler(RedundancyHandler())
    listener.registerFragmentationHandler(FragmentationHandler())

    Listeners.registerListener(listener)
