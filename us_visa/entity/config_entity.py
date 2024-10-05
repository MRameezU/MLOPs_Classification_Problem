import os
from us_visa.constants import *
from dataclasses import dataclass
from datetime import datetime

# Current timestamp for unique artifact directory naming
TIMESTAMP= datetime.now().strftime("%Y%m%d-%H%M%S")

@dataclass
class TrainingPipelineConfig:
    """Configuration class for the training pipeline.

    Attributes:
        pipline_name (str): The name of the pipeline.
        artifact_dir (str): Directory where pipeline artifacts are stored, timestamped for uniqueness.
        timestamp (str): Current timestamp for artifact versioning.
    """
    pipline_name:str= PIPELINE_NAME  # Name of the training pipeline
    artifact_dir:str= os.path.join(ARTIFACT_DIR, TIMESTAMP)  # Directory for saving artifacts
    timestamp:str= datetime.now().strftime("%Y%m%d-%H%M%S")  # Timestamp to differentiate artifacts

# Initialize the training pipeline configuration
training_pipeline_config= TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    """Configuration class for data ingestion process.

    Attributes:
        data_ingestion_dir (str): Directory where the data ingestion artifacts will be stored.
        feature_store_file_path (str): Path to the feature store file within the ingestion directory.
        training_file_path (str): Path to the ingested training dataset.
        testing_file_path (str): Path to the ingested testing dataset.
        train_test_split_ratio (float): The ratio used to split the dataset into training and testing sets.
        collection_name (str): Name of the collection where data is stored (e.g., MongoDB collection).
    """
    data_ingestion_dir:str= os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)  
    feature_store_file_path:str= os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)  
    training_file_path:str= os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)  
    testing_file_path:str= os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)  
    train_test_split_ratio: float= DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO  # Ratio for train-test split
    collection_name:str= DATA_INGESTION_COLLECTION_NAME  # Name of the data collection (e.g., in MongoDB)
