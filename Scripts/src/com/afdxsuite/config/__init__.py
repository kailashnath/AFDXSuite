from com.afdxsuite.config.parsers.icdparser import parseICD
from com.afdxsuite.application.properties import get
from com.afdxsuite.logger import general_logger
from com.afdxsuite.config.parsers import ICD_INPUT_VL
from com.afdxsuite.core.network.scapy import load_mib
from com.afdxsuite.application import PARENT_PATH

general_logger.info("Loading the ICD file")
parseICD(get("ICD_FILE"))
load_mib(PARENT_PATH + "conf/" + get("ES_MIB"))
print 'loaded mib file', PARENT_PATH + "conf/" + get("ES_MIB")