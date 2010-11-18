from com.afdxsuite.logger import initializeGeneralLogger

import ConfigParser
import os
import time

PARENT_PATH = "../../../" 
CAPTURES_PARENT_DIRECTORY = PARENT_PATH + "captures/"
LOGGER_PARENT_DIRECTORY = PARENT_PATH + "logs/"

# create the directories needed
def createDirectories():
    global CAPTURES_PARENT_DIRECTORY
    global LOGGER_PARENT_DIRECTORY

    todays_dir = time.strftime("%d %h %Y") + "/" + time.strftime("%H:%M")

    try:
        if not os.path.exists(CAPTURES_PARENT_DIRECTORY + todays_dir):
            os.makedirs(CAPTURES_PARENT_DIRECTORY + todays_dir)
        if not os.path.exists(LOGGER_PARENT_DIRECTORY + todays_dir):
            os.makedirs(LOGGER_PARENT_DIRECTORY + todays_dir)

        CAPTURES_PARENT_DIRECTORY = CAPTURES_PARENT_DIRECTORY + todays_dir
        LOGGER_PARENT_DIRECTORY = LOGGER_PARENT_DIRECTORY + todays_dir
    except Exception, ex:
        print "Exception occured creating captures directory : ", str(ex)


createDirectories()
initializeGeneralLogger(LOGGER_PARENT_DIRECTORY)

from com.afdxsuite.logger import general_logger
# load the configuration file
config = ConfigParser.RawConfigParser()
config.read(PARENT_PATH + "conf/Application.config")
general_logger.info("Configuration file initialized")

from com.afdxsuite.core.network.transmitter.TransmitHandler import TransmitHandler
from com.afdxsuite.core.network.receiver.Receiver import Receiver
from com.afdxsuite.core.network.receiver.ReceiverHandler import ReceiverHandler

class Application(object):
    transmitter = None
    receiver = None

    def __init__(self, network):
        self.transmitter = TransmitHandler(network)
        self.receiver = ReceiverHandler(network)
        self.network = network

    def boot(self):
        general_logger.info("Initialising the application")
        self.receiver.start()

    def close(self):
        general_logger.info("Terminating the application")
        self.receiver.stop()
