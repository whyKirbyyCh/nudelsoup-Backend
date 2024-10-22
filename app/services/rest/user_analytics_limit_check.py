from app.db.db_connection import DBConnection
from app.config.logger_config import Logger
from app.excpetions.db.db_connection_exception import DBConnectionException


class UserAnalyticsLimitCheckService:
    """ Class that is used to check if the user analytics limit has been met or if it needs to be refreshed. """

    logger = Logger.get_logger()
    _db_connection: DBConnection = None

    @classmethod
    def initialize_db_connection(cls):
        """Initializes the database connection."""
        if cls._db_connection is None:
            try:
                cls._db_connection = DBConnection()
                cls.logger.info("Database connection initialized.")
            except Exception as e:
                cls.logger.error(f"Failed to initialize database connection: {e}")
                raise DBConnectionException("Could not connect to the database. 1")

    @classmethod
    def close_db_connection(cls):
        """Closes the database connection."""
        if cls._db_connection is not None:
            cls._db_connection.close_connection()
            cls._db_connection = None
            cls.logger.info("Database connection closed.")

    @classmethod
    def check_user_limit(cls, user_id: str) -> bool:
        """
        Checks if the user limit has been reached.

        Returns:
            bool: True if the user limit has been reached, False otherwise.

        Raises:
            DBConnectionException: If the database connection fails.
            UserLimitsException: If the user limit has been reached.
        """
        pass