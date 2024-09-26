from us_visa.logger import logging
from us_visa.exception import USvisaException
import sys
# logging.info("Custom logging test")

try:
    error=1/0
except Exception as e:
    raise USvisaException(e,sys)