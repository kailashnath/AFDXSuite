from com.afdxsuite.application import config

def get(key):
    try:
        return config.get('GLOBAL', key);
    except:
        return None
    