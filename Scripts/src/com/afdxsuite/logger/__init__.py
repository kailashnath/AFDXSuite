import logging
import logging.handlers

general_logger = logging.getLogger("Application")

class Logger(object):
    
    script_logger = None
    loggers = {}

    def __init__(self, location, logger_name = 'Application'):

        LOG_FILE_NAME = location + "/" + logger_name + '.log'

        if self.loggers.has_key(logger_name):
            self.script_logger = self.loggers[logger_name]
        else:
            self.script_logger = logging.getLogger(logger_name)
            formatter  = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            self.script_logger.setLevel(logging.DEBUG)
    
            handler = logging.handlers.RotatingFileHandler(LOG_FILE_NAME,
                                                       # 100KB file
                                                       maxBytes = 100 * 1000,
                                                       backupCount = 30)
            handler.setFormatter(formatter)
            self.script_logger.addHandler(handler)
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            self.script_logger.addHandler(handler)
            self.loggers[logger_name] = self.script_logger

def initializeGeneralLogger(location):
    global general_logger
    general_logger = Logger(location).script_logger
    general_logger.info("Initialized logging")
