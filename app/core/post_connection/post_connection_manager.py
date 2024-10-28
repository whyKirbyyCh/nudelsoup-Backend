from typing import Dict
from app.config.logger_config import Logger
import traceback
from app.excpetions.post_connection_exception.post_connection_exception import PostConnectionException
from app.excpetions.post_connection_exception.reddit_post_connection_exception import RedditPostConnectionException
from app.excpetions.db.db_connection_exception import DBConnectionException
from app.core.post_connection.reddit_post_connection import RedditPostConnection
from app.db.db_connection import DBConnection
from pymongo.collection import Collection
from bson import ObjectId


class PostConnectionManager:
    """ Post connection manager class. """

    def __init__(self, posts: Dict[str, Dict[str, str]], user_id: str) -> None:
        """
        Initializes the PostConnectionManager class.

        Args:
            self
            posts (Dict[str, Dict[str, str]]): The posts to connect.
            user_id (str): The user ID.
        """
        self.posts: Dict[str, Dict[str, str]] = posts
        self.user_id: str = user_id

        self.logger = Logger.get_logger()
        self._db_connection: DBConnection = DBConnection()

    def connect_posts(self) -> None:
        """
        Handles all the different post connections.

        Raises:
            PostConnectionException: If an error occurs while connecting the posts.
        """
        connected_posts: Dict[str, str] = {}

        try:
            for site, content in self.posts.items():
                if site == "reddit":
                    connected_posts.update(RedditPostConnection.connect_posts_to_reddit(posts=content, user_id=self.user_id))

                else:
                    raise PostConnectionException(f"Unsupported site: {site}")

        except RedditPostConnectionException as e:
            self.logger.error(f"An error occurred while connecting the posts to Reddit: {e} \n{traceback.format_exc()}")
            raise PostConnectionException(f"An error occurred while connecting the posts to Reddit: {e}")

        except Exception as e:
            self.logger.error(f"An error occurred while connecting the posts: {e} \n{traceback.format_exc()}")
            raise PostConnectionException(f"An error occurred while connecting the posts: {e}")

    def _copy_connected_to_live_posts(self, connected_posts: Dict[str, Dict[str, str]]) -> None:
        """
        Copy the connected posts from the archive posts to the live posts.

        Args:
            connected_posts (Dict[str, Dict[str, str]]): The connected posts.

        Raises:
            PostConnectionException: If an error occurs while copying the connected posts.
            DBConnectionException: If an error occurs while copying the connected posts.
        """
        try:
            post_archive: Collection = self._db_connection.get_collection(collection_name="post_archive")
            post_live: Collection = self._db_connection.get_collection(collection_name="post_live")

            for post_id, link in connected_posts.items():
                archived_post = post_archive.find_one({"_id": ObjectId(post_id)})
                if archived_post:
                    if not post_live.find_one({"_id": ObjectId(post_id)}):
                        post_live.insert_one(archived_post)
                    else:
                        post_live.update_one({"_id": ObjectId(post_id)}, {"$set": {"redditLink": link}})

                else:
                    raise PostConnectionException(f"Could not find post with ID: {post_id}")

        except DBConnectionException as e:
            self.logger.error(f"An error occurred with the Connection to the DB while copying the connected posts: {e} \n{traceback.format_exc()}")
            raise PostConnectionException(f"An error occurred while copying the connected posts: {e}")

        except PostConnectionException as e:
            self.logger.error(f"A post was returned as connected but not found in the DB while copying the connected posts: {e} \n{traceback.format_exc()}")
            raise PostConnectionException(f"An error occurred while copying the connected posts: {e}")

        except Exception as e:
            self.logger.error(f"An error occurred while copying the connected posts: {e} \n{traceback.format_exc()}")
            raise PostConnectionException(f"An error occurred while copying the connected posts: {e}")

        finally:
            self._db_connection.close_connection()