# from us_visa.logger import logging
# from us_visa.exception import USvisaException
# import sys
# # logging.info("Custom logging test")
#
# try:
#     error=1/0
# except Exception as e:
#     raise USvisaException(e,sys)

# training pipeline test and Data Validation pipeline test
from us_visa.pipline.training_pipeline import TrainPipeline

object = TrainPipeline()
object.run_pipeline()



