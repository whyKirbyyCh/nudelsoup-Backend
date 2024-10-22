from app.db.db_connection import DBConnection
from app.excpetions.db.db_connection_exception import DBConnectionException
from app.config.logger_config import Logger
from typing import List
from app.models.post import Post
from app.excpetions.post_creation_exception.post_archive_excpetion import PostArchiveException
import traceback


class PostArchiveService:

    _db_connection = None
    logger = Logger.get_logger()

    @classmethod
    def _initialize_db_connection(cls):
        """Initializes the database connection."""
        if cls._db_connection is None:
            try:
                cls._db_connection = DBConnection()
                cls.logger.info("Database connection initialized.")
            except Exception as e:
                cls.logger.error(f"Failed to initialize database connection: {e}")
                raise DBConnectionException("Could not connect to the database. 1")

    @classmethod
    def _close_db_connection(cls):
        """Closes the database connection."""
        if cls._db_connection is not None:
            cls._db_connection.close_connection()
            cls._db_connection = None
            cls.logger.info("Database connection closed.")

    @classmethod
    def archive_posts(cls, posts: List[Post]) -> bool:
        """
        Archives the posts.

        Args:
            posts (List[Post]): The list of posts to archive.

        Returns:
            bool: True if the posts were archived successfully, False otherwise.

        Raises:
            DBConnectionException: If the database connection fails.
        """
        cls._initialize_db_connection()

        try:
            collection = cls._db_connection.get_collection(collection_name="post_archive")

            post_dicts = [post.to_dict() for post in posts]

            collection.insert_many(post_dicts)

            cls.logger.info("Posts archived successfully.")

            return True
        except DBConnectionException as e:
            cls.logger.error(f"Failed to archive posts: {e}")
            raise PostArchiveException(f"Failed to archive posts: {e}\n{traceback.format_exc()}") from e

        except Exception as e:
            cls.logger.error(f"Failed to archive posts: {e}")
            raise PostArchiveException(f"Failed to archive posts: {e}\n{traceback.format_exc()}") from e

        finally:
            cls._close_db_connection()
