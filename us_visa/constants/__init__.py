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

FILE_NAME="usvisa.csv"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"

MODEL_FILE_NAME="model.pkl"

# Data Ingestion constant starting with DATA_INGESTION VAR NAME

DATA_INGESTION_COLLECTION_NAME= "visa_data"
DATA_INGESTION_DIR_NAME="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR= "feature_store"
DATA_INGESTION_INGESTED_DIR="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2 # 80% training and 20% validation
