import sys
from us_visa.components.data_ingestion import DataIngestion
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.exception import USvisaException
from us_visa.logger import logging


class TrainPipeline:
    """Class for managing the training pipeline, which includes data ingestion and the orchestration of different training phases."""

    def __init__(self):
        """
        Initialize the training pipeline with configurations.

        Attributes:
            data_ingestion_config (DataIngestionConfig): Configuration settings for data ingestion.
        """
        self.data_ingestion_config = DataIngestionConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Start the data ingestion process, fetching data from MongoDB, splitting it into train and test sets,
        and returning the artifact containing the file paths.

        Returns:
            DataIngestionArtifact: An artifact containing file paths of the train and test sets.

        Raises:
            USvisaException: If any error occurs during data ingestion.
        """
        try:
            logging.info("Entered the `start_data_ingestion` method of `class TrainPipeline`.")
            logging.info("Starting data ingestion by fetching the data from MongoDB.")

            # Initiate data ingestion
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Data ingestion completed successfully. Train and test sets are prepared.")
            logging.info("Exiting the `start_data_ingestion` method of `class TrainPipeline`.")

            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e

    def run_pipeline(self) -> None:
        """
        Run the entire training pipeline by first initiating the data ingestion process.

        Raises:
            USvisaException: If any error occurs while running the pipeline.
        """
        try:
            logging.info("Starting the training pipeline.")

            # Start the data ingestion process
            data_ingestion_artifact = self.start_data_ingestion()

            logging.info("Training pipeline execution completed successfully.")
        except Exception as e:
            raise USvisaException(e, sys) from e
