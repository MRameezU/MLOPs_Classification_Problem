import sys
from us_visa.components.data_ingestion import DataIngestion
from us_visa.entity.config_entity import DataIngestionConfig, DataValidationConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.components.data_validation import DataValidation


class TrainPipeline:
    """
    Manages the entire training pipeline process, which includes data ingestion,
    data validation, and orchestrating subsequent training phases.
    """

    def __init__(self):
        """
        Initializes the training pipeline with configurations for both data ingestion and validation.

        Class Attributes:
            data_ingestion_config (DataIngestionConfig): Stores configuration settings required for the data ingestion process.
            data_validation_config (DataValidationConfig): Stores configuration settings required for the data validation process.
        """
        self.data_ingestion_config = DataIngestionConfig()  # Initialize data ingestion config
        self.data_validation_config = DataValidationConfig()  # Initialize data validation config

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiates the data ingestion process, which fetches data from the data source (e.g., MongoDB),
        splits it into training and testing datasets, and returns the file paths of these datasets.

        Returns:
            DataIngestionArtifact: An object containing file paths of the train and test datasets.

        Raises:
            USvisaException: If any error occurs during the data ingestion process.
        """
        try:
            logging.info("Entered the `start_data_ingestion` method of `TrainPipeline`.")
            logging.info("Starting data ingestion by fetching the data from MongoDB.")

            # Create an instance of DataIngestion and initiate the ingestion process
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Data ingestion completed successfully. Train and test datasets are prepared.")
            logging.info("Exiting the `start_data_ingestion` method of `TrainPipeline`.")

            return data_ingestion_artifact  # Return the artifact containing dataset paths
        except Exception as e:
            raise USvisaException(e, sys) from e  # Handle and log errors

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        Initiates the data validation process, ensuring that the ingested data conforms
        to expected schema rules and checking for dataset drift.

        Args:
            data_ingestion_artifact (DataIngestionArtifact): The artifact containing paths to the ingested train and test data.

        Returns:
            DataValidationArtifact: An artifact containing the results of the validation process.

        Raises:
            USvisaException: If any error occurs during the data validation process.
        """
        logging.info("Entered the `start_data_validation` method of `TrainPipeline`.")
        try:
            # Create an instance of DataValidation and initialize the validation process
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initialize_data_validation()

            logging.info("Data validation completed successfully.")
            logging.info("Exiting the `start_data_validation` method of `TrainPipeline`.")

            return data_validation_artifact  # Return the artifact containing validation results
        except Exception as e:
            raise USvisaException(e, sys) from e  # Handle and log errors

    def run_pipeline(self) -> None:
        """
        Runs the entire training pipeline, starting from data ingestion to data validation.

        Steps:
            1. Initiates data ingestion.
            2. Performs data validation after ingestion.
            3. (In future implementations) Executes further training and evaluation tasks.

        Raises:
            USvisaException: If any error occurs while executing any step in the pipeline.
        """
        try:
            logging.info("Starting the training pipeline.")

            # Step 1: Start data ingestion
            data_ingestion_artifact = self.start_data_ingestion()

            # Step 2: Start data validation
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

            # Additional steps (e.g., model training) will follow here in future implementations.

            logging.info("Training pipeline execution completed successfully.")
        except Exception as e:
            raise USvisaException(e, sys) from e  # Handle and log errors

