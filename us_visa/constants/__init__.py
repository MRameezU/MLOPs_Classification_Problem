from datetime import date
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()
# Connection URL for the DB

DATABASE_NAME = os.getenv("DATABASE_NAME")

COLLECTION_NAME=os.getenv("COLLECTION_NAME")

# Get the MongoDB URI from the environment variable
MONGODB_URL_KEY=os.getenv("CONNECTION_URL") # connection string


PIPELINE_NAME= "usvisa"
ARTIFACT_DIR= "artifact"


TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"

FILE_NAME="usvisa.csv"
MODEL_FILE_NAME="model.pkl"


# DataDrift
TARGET_COLUMN = "case_status" #
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME="preprocessing.pkl" #preprocessing pipeline object
SCHEMA_FILE_PATH=os.path.join("config","schema.yaml")#schema file path url

# Data Ingestion constant starting with DATA_INGESTION VAR NAME

DATA_INGESTION_COLLECTION_NAME= "visa_data"
DATA_INGESTION_DIR_NAME="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR= "feature_store"
DATA_INGESTION_INGESTED_DIR="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2 # 80% training and 20% validation

# data validation related constants
DATA_VALIDATION_DIR_NAME="data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME="report.yaml"