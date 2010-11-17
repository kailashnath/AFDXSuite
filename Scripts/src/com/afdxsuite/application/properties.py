from com.afdxsuite.application import config
from com.afdxsuite.logger import general_logger

def get(key):
    try:
        return config.get('GLOBAL', str(key).lower());
    except Exception, ex:

        general_logger.error('No properties key found for : ' + key)
        print "Exception at reading properties file", str(ex)
        return None
    