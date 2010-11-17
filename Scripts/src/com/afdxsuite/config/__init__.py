from com.afdxsuite.config.parsers.icdparser import parseICD
from com.afdxsuite.application.properties import get
from com.afdxsuite.logger import general_logger
from com.afdxsuite.config.parsers import ICD_INPUT_VL

general_logger.info("Loading the ICD file")
parseICD(get("ICD_FILE"))
