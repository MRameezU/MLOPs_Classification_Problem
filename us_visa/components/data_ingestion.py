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
    """Class responsible for data ingestion process, which includes exporting data from MongoDB,
    saving it to a feature store, and splitting the data into training and testing sets."""

    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """
        Initializes the DataIngestion instance with configuration.

        Args:
            data_ingestion_config (DataIngestionConfig): Configuration object for data ingestion.

        Raises:
            USvisaException: If there is an error during initialization.
        """
        try:
            self.data_ingestion_config = data_ingestion_config
            logging.info(f"Initialized DataIngestion with config: {data_ingestion_config}")
        except Exception as e:
            raise USvisaException(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Exports data from MongoDB into a pandas DataFrame and saves it to a feature store (CSV file).

        Returns:
            DataFrame: The DataFrame containing the exported data.

        Raises:
            USvisaException: If there is an error during data export or file saving.
        """
        try:
            logging.info("Starting data export from MongoDB.")
            usvisa_data = USvisaData()

            # Export data from MongoDB to DataFrame
            dataframe = usvisa_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"Data exported from MongoDB with shape: {dataframe.shape}")

            # Ensure feature store directory exists
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Directory for feature store created at: {dir_path}")

            # Save the DataFrame to a CSV file
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(f"Data saved to feature store at: {feature_store_file_path}")
            return dataframe

        except Exception as e:
            raise USvisaException(e, sys)

    def split_data_as_train_test(self, dataframe: DataFrame):
        """
        Splits the input DataFrame into training and testing sets and saves them to disk.

        Args:
            dataframe (DataFrame): The input DataFrame to be split.

        Raises:
            USvisaException: If there is an error during the split or file saving process.
        """
        try:
            logging.info("Performing train-test split on the dataframe.")
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio)

            logging.info(
                f"Train-test split completed with train shape: {train_set.shape}, test shape: {test_set.shape}")

            # Ensure the directory for saving train/test sets exists
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(name=dir_path, exist_ok=True)
            logging.info(f"Directory for train/test files created at: {dir_path}")

            # Save train and test datasets to CSV
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info(f"Train data saved to: {self.data_ingestion_config.training_file_path}")
            logging.info(f"Test data saved to: {self.data_ingestion_config.testing_file_path}")

        except Exception as e:
            raise USvisaException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Orchestrates the data ingestion process by exporting the data and splitting it into train and test sets.

        Returns:
            DataIngestionArtifact: An artifact containing paths to the train and test datasets.

        Raises:
            USvisaException: If there is an error during the data ingestion process.
        """
        try:
            logging.info("Initiating data ingestion process.")

            # Step 1: Export data to feature store
            dataframe = self.export_data_into_feature_store()
            logging.info("Data successfully exported from MongoDB.")

            # Step 2: Split the data into train and test sets
            self.split_data_as_train_test(dataframe=dataframe)
            logging.info("Train-test split performed successfully.")

            # Create data ingestion artifact
            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info(f"Data ingestion completed successfully. Artifact created: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise USvisaException(e, sys) from e
