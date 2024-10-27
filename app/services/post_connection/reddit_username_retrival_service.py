from app.config.logger_config import Logger
from app.db.db_connection import DBConnection
from app.excpetions.db.db_connection_exception import DBConnectionException
import traceback
from pymongo.collection import Collection
from typing import Dict


class RedditUsernameRetrivalService:
    """ Given a userId, returns the username of the user. """

    logger = Logger.get_logger()
    _db_connection: DBConnection = DBConnection()

    @classmethod
    def get_username(cls, user_id: str) -> str:
        """
        Given a userId, returns the username of the user.

        Args:
            user_id (str): The user id.

        Returns:
            str: The username of the user.

        Raises:
            DBConnectionException: If the database connection fails.
        """
        try:
            collection: Collection = cls._db_connection.get_collection("accounts")
            user: Dict = collection.find_one({"userId": user_id})

            return user["redditUsername"]

        except DBConnectionException:
            cls.logger.error("DB connection error.")
            raise DBConnectionException("Could not connect to the database while getting username.")

        except Exception as e:
            cls.logger.error(f"An error occurred while getting username: {e} \n{traceback.format_exc()}")
            raise DBConnectionException(f"An error occurred while getting username: {e}")

