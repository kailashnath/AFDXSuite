from com.afdxsuite.application import Application
from com.afdxsuite.scripts.Script001 import Script001

import time
from com.afdxsuite.scripts.Script002 import Script002
from com.afdxsuite.scripts.Script003 import Script003
from com.afdxsuite.scripts.Script004 import Script004
from com.afdxsuite.core.network import NETWORK_A, NETWORK_AB
from com.afdxsuite.scripts.Script005 import Script005
from com.afdxsuite.scripts.Script006 import Script006
from com.afdxsuite.scripts.Script008 import Script008
from com.afdxsuite.scripts.Script009 import Script009
from com.afdxsuite.scripts.Script010 import Script010
from com.afdxsuite.scripts.Script011 import Script011
from com.afdxsuite.scripts.Script012 import Script012
from com.afdxsuite.scripts.Script013 import Script013

if __name__ == '__main__':
    application = Application(NETWORK_AB)
    application.boot()
    script = Script013(application)
    script.run()
    script.stop()
    application.close()
