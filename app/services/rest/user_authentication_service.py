from app.excpetions.rest.user_authentication_excpetion import UserAuthenticationException
from app.excpetions.rest.invalid_user_credentials_exception import InvalidUserCredentialsException
from app.excpetions.rest.invalid_token_exception import InvalidTokenException
from app.excpetions.db.db_connection_exception import DBConnectionException
from app.db.db_connection import DBConnection
from app.config.logger_config import Logger
from typing import Tuple, Dict
from bson import ObjectId
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import traceback


class UserAuthenticationService:
    """
    Class that provides methods for user authentication.
    """

    load_dotenv(override=True)
    logger = Logger.get_logger()
    _db_connection: DBConnection = DBConnection()

    @classmethod
    def authenticate_user(cls, token: str) -> Tuple[bool, str]:
        """
        Authenticates the user.

        Args:
            token (str): The token of the user.

        Returns:
            bool: True if the user is authenticated, False otherwise.

        Raises:
            UserAuthenticationException: If the user is not authenticated.
        """
        user_id: str
        hashed_pw: str

        try:
            key: str = os.getenv("SECRET_KEY")
            cipher: Fernet = Fernet(key)

            decrypted_data: str = cipher.decrypt(token.encode()).decode()
            user_id, hashed_pw = decrypted_data.split(":")

            if not cls._check_credentials(user_id, hashed_pw):
                raise InvalidUserCredentialsException("User credentials are invalid.")

            return True, user_id

        except UserAuthenticationException:
            cls.logger.error(f"User authentication failed for token: {token}, {traceback.format_exc()}")
            raise UserAuthenticationException("User is not allowed to access this resource.")

        except InvalidUserCredentialsException:
            cls.logger.error(f"Token decryption returned an invalid user credentials: {token}")
            raise UserAuthenticationException("Invalid user credentials.")

        except InvalidTokenException:
            cls.logger.error(f"Token could not be verified: {token}, {traceback.format_exc()}")
            raise UserAuthenticationException("Invalid token.")

    @classmethod
    def _check_credentials(cls, user_id: str, hashed_pw: str) -> bool:
        """
        Checks if the user ID is valid.

        Args:
            user_id (str): The user ID.
            hashed_pw (str): The hashed password.

        Returns:
            bool: True if the user ID is valid, False otherwise.

        Raises:
            InvalidUserCredentialsException: If the user credentials are invalid.
            DBConnectionException: If the database connection fails.
        """
        try:
            cls._db_connection.get_collection(collection_name="users")
            user: Dict = cls._db_connection.get_collection(collection_name="users").find_one({"_id": ObjectId(user_id)})

            if not user:
                raise InvalidUserCredentialsException("User not found.")

            if user["password"] != hashed_pw:
                raise InvalidUserCredentialsException("Password did not match.")

            return True

        except InvalidUserCredentialsException:
            raise UserAuthenticationException("Invalid user credentials.")

        except DBConnectionException:
            raise UserAuthenticationException("Failed to connect to the database.")
