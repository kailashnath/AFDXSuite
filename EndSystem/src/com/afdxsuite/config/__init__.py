from com.afdxsuite.config.parsers.icdparser import parseICD
from com.afdxsuite.application.properties import get
from com.afdxsuite.logging import afdxLogger

afdxLogger.info("Loading the ICD file")
parseICD(get("ICD_FILE"))