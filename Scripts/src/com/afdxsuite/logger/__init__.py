import logging
import logging.handlers

general_logger = logging.getLogger("Application")

class Logger(object):
    
    script_logger = None

    def __init__(self, location, logger_name = 'Application'):

        LOG_FILE_NAME = location + "/" + logger_name + '.log'

        self.script_logger = logging.getLogger(logger_name)
        formatter  = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.script_logger.setLevel(logging.DEBUG)

        handler = logging.handlers.RotatingFileHandler(LOG_FILE_NAME,
                                                       # 10KB file
                                                       maxBytes = 10 * 1000,
                                                       backupCount = 5)
        handler.setFormatter(formatter)
        self.script_logger.addHandler(handler)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.script_logger.addHandler(handler)

def initializeGeneralLogger(location):
    global general_logger
    general_logger = Logger(location).script_logger
    general_logger.info("Initialized logging")
