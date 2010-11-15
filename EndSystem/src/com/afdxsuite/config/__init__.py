from com.afdxsuite.config.parsers.icdparser import parseICD
from com.afdxsuite.application.properties import get
from com.afdxsuite.logging import afdxLogger
from com.afdxsuite.config.parsers import ICD_INPUT_VL

afdxLogger.info("Loading the ICD file")
parseICD(get("ICD_FILE"))
