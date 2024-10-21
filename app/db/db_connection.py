from pymongo import MongoClient
from dotenv import load_dotenv
import os
from app.config.logger_config import Logger
from app.excpetions.db.db_connection_exception import DBConnectionException


class DBConnection:
    """ Class that is used to connect to the MongoDB database. """

    load_dotenv(override=True)
    logger = Logger.get_logger()

    def __init__(self) -> None:
        """ Initializes the DBConnection class."""
        self.client: MongoClient = MongoClient(os.getenv("MONGODB_URI"))

    def get_collection(self, collection_name: str, database_name: str = "users") -> MongoClient:
        """ Returns the collection with the given name. """
        try:
            self.client.admin.command('ping')
            return self.client[database_name][collection_name]

        except Exception as ex:
            self.logger.error(f"An error occurred while connecting to the database: {ex}")
            raise DBConnectionException(f"An error occurred while connecting to the database: {ex}")

    def close_connection(self) -> None:
        """ Closes the connection to the database. """
        self.client.close()