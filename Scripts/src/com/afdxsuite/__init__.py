from com.afdxsuite.application import Application
from com.afdxsuite.core.network import NETWORK_AB
from com.afdxsuite.logger import general_logger

import sys, traceback

if __name__ == '__main__':
    application = Application(NETWORK_AB)
    try:
        application.boot()
        while True:
            script = None
            try:
                choice = raw_input("Please enter the script number (1 - 24) or"\
                                   " 0 to exit : ")
                choice = int(choice)
                if choice == 0:
                    break
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
