import os
import sys


from pandas import DataFrame
from sklearn.model_selection import train_test_split

from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.data_access.usvisa_data import USvisaData


class DataIngestion:
    def __init__(self,data_ingestion_config=DataIngestionConfig()):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise USvisaException(e,sys)


    def export_data_into_feature_store(self):
        try:
            logging.info(f"Exporting data from MongoDB")
            usvisa_data=USvisaData()
            dataframe = usvisa_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"Saving exported dataframe: {dataframe.shape}")
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise USvisaException(e,sys)


    def split_data_as_train_test(self,dataframe: DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("performed train test split on the dataframe")
            logging.info("Exit split_data_as_train_test method of DataIngestion class")
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(name=dir_path,exist_ok=True)
            logging.info("Exported train and test file paths")
        except Exception as e:
            raise USvisaException(e,sys) from e

    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_data_into_feature_store()
            logging.info("Received data from MongoBD")
            self.split_data_as_train_test(dataframe=dataframe)

            logging.info("Performed train and test split on Dataset")

            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )

            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e,sys) from e