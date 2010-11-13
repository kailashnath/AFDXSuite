from com.afdxsuite.application import config

def get(key):
    try:
        return config.get('GLOBAL', str(key).lower());
    except Exception, ex:
        print "Exception at reading properties file", str(ex)
        return None
    