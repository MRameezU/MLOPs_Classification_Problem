import sys
import pandas as pd
import numpy as np
from typing import Optional

from us_visa.configuration.mongo_db_connection import MongoDBClient
from us_visa.constants import DATABASE_NAME
from us_visa.exception import USvisaException


class USvisaData:
    """A class for interacting with the US visa MongoDB database and exporting collections as DataFrames."""

    def __init__(self):
        """
        Initializes a connection to the MongoDB database.

        Raises:
            USvisaException: If there is an error in connecting to the MongoDB database.
        """
        try:
            # Initialize MongoDB client with the specified database
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            # Raise a custom exception if the connection fails
            raise USvisaException(e, sys)

    def export_collection_as_dataframe(self, collection_name: str,
                                       database_name: Optional[str] = None) -> pd.DataFrame:
        """Exports a MongoDB collection as a pandas DataFrame.

        Args:
            collection_name (str): The name of the MongoDB collection to export.
            database_name (Optional[str]): The name of the MongoDB database. If not provided, the default database is used.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the data from the MongoDB collection.

        Raises:
            USvisaException: If there is an error in retrieving data from the collection or during processing.
        """
        try:
            # If no database name is provided, use the default database
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            # Convert the MongoDB collection to a pandas DataFrame
            df = pd.DataFrame(list(collection.find()))
            # collection.find({}, {"_id": 0})  # This excludes '_id' at the database level

            # Drop the '_id' column if it exists, as it's not required
            if "_id" in df.columns.to_list():
                df = df.drop(columns=['_id'], axis=1)
                collection.find({}, {"_id": 0})  # This excludes '_id' at the database level

            # Replace 'na' strings with np.nan to handle missing values
            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            # Raise a custom exception in case of any failure during the export process
            raise USvisaException(e, sys)
