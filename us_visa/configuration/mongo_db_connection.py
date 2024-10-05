import logging
import os
import pymongo
import sys
import certifi

from us_visa.constants import DATABASE_NAME, MONGODB_URL_KEY
from us_visa.exception import USvisaException

ca = certifi.where()


class MongoDBClient:
    """
    A MongoDB client class to handle connections to a MongoDB database.

    The client uses environment variables to fetch the MongoDB URL and connects securely using the `pymongo` client
    with TLS certificate verification.

    Attributes:
        client (pymongo.MongoClient): A shared MongoDB client instance used across all instances of `MongoDBClient`.
        database (pymongo.database.Database): The specific database to interact with, based on `database_name`.
        database_name (str): The name of the database to connect to.

    Args:
        database_name (str): Name of the database to connect to (default is `DATABASE_NAME` from constants).

    Raises:
        USvisaException: If the MongoDB URL is not set in the environment variables or if the connection fails.

    Example:
        mongo_client = MongoDBClient()
        collection = mongo_client.database['collection_name']
        documents = collection.find({})
    """

    client = None

    def __init__(self, database_name=DATABASE_NAME):
        """
        Initializes the MongoDBClient with a connection to the specified database.

        This constructor checks if the MongoDB URL is available in the environment variables.
        If not, it raises an exception. It uses a TLS certificate to connect securely to the MongoDB instance.

        Args:
            database_name (str): Name of the database to connect to (defaults to `DATABASE_NAME`).

        Raises:
            USvisaException: If an error occurs during MongoDB connection initialization.
        """
        try:
            if MongoDBClient.client is None:
                # Fetch MongoDB URL from environment variable
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set in the environment variables")

                # Initialize the MongoDB client with TLS CA file for secure connection
                MongoDBClient.client = pymongo.MongoClient(host=mongo_db_url, tlsCAFile=ca)

            # Assign the shared client instance and connect to the database
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successful")
        except Exception as e:
            raise USvisaException(error_message=e, error_detail=sys)
