from com.afdxsuite.application import Application
from com.afdxsuite.scripts.Script001 import Script001

import time

if __name__ == '__main__':
    application = Application('A')
    application.boot()
    script = Script001(application)
    script.run()
    script.stop()
    print 'script stopped'
    application.close()

