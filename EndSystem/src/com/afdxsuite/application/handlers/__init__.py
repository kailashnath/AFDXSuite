from com.afdxsuite.application.TestResponder.RSET import RSET
from com.afdxsuite.application.TestResponder.ERPQ import ERPQ
from com.afdxsuite.application.TestResponder.EIPC import EIPC
from com.afdxsuite.application.TestResponder.ESAP import ESAP
from com.afdxsuite.application.TestResponder.TCRQ import TCRQ
from com.afdxsuite.application.TestResponder.RRPC import RRPC


COMMAND_HANDLERS = {'RSET' : RSET,
                    'ERPQ' : ERPQ,
                    'EIPC' : EIPC,
                    'ESAP' : ESAP,
                    'TCRQ' : TCRQ,
                    'RRPC' : RRPC}