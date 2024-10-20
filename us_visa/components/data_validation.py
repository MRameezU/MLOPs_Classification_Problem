import json
import sys

import pandas as pd
from pandas import DataFrame

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from pandas.core.interchange.dataframe_protocol import DataFrame

from us_visa.constants import SCHEMA_FILE_PATH
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.exception import USvisaException
from us_visa.utils.main_utils import read_yaml_file
from us_visa.logger import logging


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e,sys)


    def validation_number_of_columns(self,dataframe:DataFrame):
        try:
            status=len(dataframe.columns)==len(self._schema_config["columns"])
            logging.info(f"Is required Column present: [{status}]")
        except Exception as e:
            raise USvisaException(e, sys)

    def is_column_exist(self,df:DataFrame):
        try:
            dataframe_columns=df.columns
            missing_numerical_columns=[]
            missing_categorical_columns=[]

            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)
            if len(missing_numerical_columns)>0:
                logging.info(f"Missing numerical column: {missing_numerical_columns}")

            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if len(missing_categorical_columns)>0:
                logging.info(f"Missing categorical column: {missing_categorical_columns}")

            return False if len(missing_numerical_columns)>0 or len(missing_categorical_columns)>0 else True

        except Exception as e:
            raise USvisaException(e, sys)

    def detect_dataset_drift(self,reference_df:DataFrame,current_df:DataFrame):
        try:
            ...
        except Exception as e:
            raise USvisaException(e, sys)

