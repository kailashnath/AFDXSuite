from com.afdxsuite.application import Application
from com.afdxsuite.scripts.Script001 import Script001

import time
from com.afdxsuite.scripts.Script002 import Script002
from com.afdxsuite.scripts.Script003 import Script003
from com.afdxsuite.scripts.Script004 import Script004
from com.afdxsuite.core.network import NETWORK_A, NETWORK_AB
from com.afdxsuite.scripts.Script005 import Script005

if __name__ == '__main__':
    application = Application(NETWORK_AB)
    application.boot()
    script = Script005(application)
    script.run()
    script.stop()
    print 'script stopped'
    application.close()

