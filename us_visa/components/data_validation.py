import json
import sys
import pandas as pd
from pandas import DataFrame
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

from us_visa.constants import SCHEMA_FILE_PATH
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.exception import USvisaException
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
from us_visa.logger import logging


class DataValidation:
    """
    A class to perform data validation tasks such as validating column numbers,
    checking for missing columns, and detecting data drift.

    Attributes:
        data_ingestion_artifact (DataIngestionArtifact): Contains paths to the train and test datasets.
        data_validation_config (DataValidationConfig): Configuration for data validation, including schema and drift report path.
        _schema_config (dict): Schema configuration loaded from a YAML file.
    """

    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        """
        Initializes the DataValidation class by loading the schema configuration.

        Args:
            data_ingestion_artifact (DataIngestionArtifact): Contains paths to ingested datasets.
            data_validation_config (DataValidationConfig): Contains validation configurations such as drift report file path.

        Raises:
            USvisaException: If any error occurs during initialization.
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact  # Path to ingested data
            self.data_validation_config = data_validation_config  # Data validation config (drift report path)
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)  # Load schema config from YAML
        except Exception as e:
            raise USvisaException(e, sys)

    def validate_number_of_columns(self, dataframe: DataFrame):
        """
        Validates if the number of columns in the dataframe matches the schema.

        Args:
            dataframe (DataFrame): The dataframe to be validated.

        Returns:
            bool: True if column count matches the schema, False otherwise.

        Raises:
            USvisaException: If any error occurs during validation.
        """
        try:
            # Check if the number of columns in the dataframe matches the schema configuration
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Is required Column present: [{status}]")
        except Exception as e:
            raise USvisaException(e, sys)

    def is_column_exist(self, df: DataFrame):
        """
        Checks if all required numerical and categorical columns exist in the dataframe.

        Args:
            df (DataFrame): The dataframe to check.

        Returns:
            bool: True if all required columns exist, False otherwise.

        Raises:
            USvisaException: If any error occurs during column existence check.
        """
        try:
            dataframe_columns = df.columns  # List of dataframe columns
            missing_numerical_columns = []
            missing_categorical_columns = []

            # Check for missing numerical columns
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)
            if len(missing_numerical_columns) > 0:
                logging.info(f"Missing numerical column: {missing_numerical_columns}")

            # Check for missing categorical columns
            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)
            if len(missing_categorical_columns) > 0:
                logging.info(f"Missing categorical column: {missing_categorical_columns}")

            # Return False if any required column is missing
            return False if len(missing_numerical_columns) > 0 or len(missing_categorical_columns) > 0 else True

        except Exception as e:
            raise USvisaException(e, sys)

    @staticmethod
    def read_data(file_path) -> DataFrame:
        """
        Reads a CSV file into a pandas DataFrame.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            DataFrame: Loaded dataframe from CSV file.

        Raises:
            USvisaException: If any error occurs during file reading.
        """
        try:
            # Read CSV file using pandas
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e, sys)

    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame):
        """
        Detects data drift between the reference and current datasets using Evidently's DataDriftProfile.

        Args:
            reference_df (DataFrame): The reference dataframe (usually training data).
            current_df (DataFrame): The current dataframe (usually test data).

        Returns:
            bool: True if dataset drift is detected, False otherwise.

        Raises:
            USvisaException: If any error occurs during drift detection.
        """
        try:
            # Create a data drift profile using Evidently
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(reference_data=reference_df, current_data=current_df)

            # Convert the drift profile to JSON format
            report = data_drift_profile.json()
            json_report = json.loads(report)

            # Write the drift report to a YAML file
            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report)

            # Extract drift metrics from the report
            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]

            logging.info(f"{n_drifted_features} / {n_features} drift detected !!")

            # Return drift status (True/False)
            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]

            return drift_status
        except Exception as e:
            raise USvisaException(e, sys)

    def initialize_data_validation(self) -> DataValidationArtifact:
        """
        Performs data validation, including column checks and data drift detection.

        Returns:
            DataValidationArtifact: The result of the validation process, including status and message.

        Raises:
            USvisaException: If any error occurs during data validation initialization.
        """
        try:
            validation_error_msg = ""
            logging.info("Starting data validation")

            # Read train and test data
            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.train_file_path),
                                 DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))

            # Validate number of columns in train and test datasets
            status = self.validate_number_of_columns(dataframe=train_df)
            logging.info(f"All required columns present in training dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."

            status = self.validate_number_of_columns(dataframe=test_df)
            logging.info(f"All required columns present in testing dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."

            # Check if all required columns exist in train and test datasets
            status = self.is_column_exist(df=train_df)
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."

            status = self.is_column_exist(df=test_df)
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."

            # If no validation errors, perform drift detection
            validation_status = len(validation_error_msg) == 0
            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logging.info(f"Drift detected.")
                    validation_error_msg = "Drift detected"
                else:
                    validation_error_msg = "Drift not detected"
            else:
                logging.info(f"Validation_error: {validation_error_msg}")

            # Create a DataValidationArtifact to hold validation results
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise USvisaException(e, sys)
