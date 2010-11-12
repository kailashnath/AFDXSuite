import logging
import logging.handlers

LOG_FILE_NAME = 'example.log'

afdxLogger = logging.getLogger('EndSystem')
formatter  = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
afdxLogger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(LOG_FILE_NAME,
                                               maxBytes = 1 * 1000,
                                               backupCount = 5)
handler.setFormatter(formatter)
afdxLogger.addHandler(handler)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
afdxLogger.addHandler(handler)

print 'initialized logger'