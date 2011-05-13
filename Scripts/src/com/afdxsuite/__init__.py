from com.afdxsuite.application import Application
from com.afdxsuite.core.network import NETWORK_AB
from com.afdxsuite.scripts.Script001 import Script001
from com.afdxsuite.scripts.Script002 import Script002
from com.afdxsuite.scripts.Script003 import Script003
from com.afdxsuite.scripts.Script004 import Script004
from com.afdxsuite.scripts.Script005 import Script005
from com.afdxsuite.scripts.Script006 import Script006
from com.afdxsuite.scripts.Script008 import Script008
from com.afdxsuite.scripts.Script009 import Script009
from com.afdxsuite.scripts.Script010 import Script010
from com.afdxsuite.scripts.Script011 import Script011
from com.afdxsuite.scripts.Script012 import Script012
from com.afdxsuite.scripts.Script013 import Script013
from com.afdxsuite.scripts.Script014 import Script014
from com.afdxsuite.scripts.Script015 import Script015
from com.afdxsuite.scripts.Script016 import Script016
from com.afdxsuite.scripts.Script017 import Script017
from com.afdxsuite.scripts.Script018 import Script018
from com.afdxsuite.scripts.Script019 import Script019
from com.afdxsuite.scripts.Script020 import Script020
from com.afdxsuite.scripts.Script021 import Script021
from com.afdxsuite.scripts.Script022 import Script022
from com.afdxsuite.scripts.Script023 import Script023
from com.afdxsuite.scripts.Script024 import Script024

from com.afdxsuite.application.analyzer.CaptureAnalyzer import Analyzer
import time

from com.afdxsuite.logger import general_logger

import sys, traceback

if __name__ == '__main__':
    application = Application(NETWORK_AB)
    try:
        # this is removed as we have resorted to capturing the packets
        # externally via scripts
        #application.boot()
        while True:
            script = None
            try:
                application.transmitter.reset()
                choice = raw_input("Please enter the script number (1 - 24) or"\
                                   " 25 for Analyzer or 0 to exit : ")
                if choice == "":
                    continue

                choice = int(choice)
                if choice == 0:
                    break
                elif choice == 25:
                    analyzer = Analyzer()
                    analyzer.start()
                    continue
                elif choice > 25 or choice < 0 or choice == 7:
                    general_logger.warning("Invalid option %d" % choice)
                    continue
                script = eval("Script%03d" % choice)(application)
                script.run()
                script.stop()
            except KeyboardInterrupt:
                    if script != None:
                        script.stop()
            except Exception, ex:
                general_logger.error("Could not execute the script. : %s" % \
                                     (str(ex)))
                traceback.print_exc(file=sys.stdout)

    except KeyboardInterrupt:
        pass
    finally:
        application.close()
