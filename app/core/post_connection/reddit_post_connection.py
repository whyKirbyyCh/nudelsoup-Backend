from typing import Dict
from app.excpetions.post_connection_exception.reddit_post_connection_exception import RedditPostConnectionException
from app.config.logger_config import Logger
import praw
import os
from dotenv import load_dotenv
from app.services.post_connection.reddit_username_retrival_service import RedditUsernameRetrivalService
from difflib import SequenceMatcher
from typing import List, Optional
from app.db.db_connection import DBConnection
from app.excpetions.db.db_connection_exception import DBConnectionException
from pymongo.collection import Collection
import traceback
from bson import ObjectId


class RedditPostConnection:
    """ Class for Reddit post connection. """

    logger = Logger.get_logger()
    load_dotenv(override=True)
    _db_connection: DBConnection = DBConnection()

    @classmethod
    def connect_posts_to_reddit(cls, posts: Dict[str, str], user_id: str) -> Dict[str, str]:
        """
        Connect posts to Reddit by finding the most similar Reddit post for each content entry.

        Args:
            posts (Dict[str, str]): The dictionary of posts to connect.
            user_id (str): The ID of the user.

        Returns:
            Dict[str, str]: A dictionary with post_id as keys and the Reddit link as values.

        Raises:
            RedditPostConnectionException: If an error occurs while connecting the posts to Reddit.
        """
        connected_posts: Dict[str, str] = {}

        try:
            reddit: praw.Reddit = praw.Reddit(
                client_id=os.getenv("REDDIT_CLIENT_ID"),
                client_secret=os.getenv("REDDIT_SECRET_KEY"),
                user_agent=os.getenv("REDDIT_USER_AGENT")
            )

            username: str = RedditUsernameRetrivalService.get_username(user_id)
            redditor: praw.reddit.Redditor = reddit.redditor(username)

            reddit_posts: List[praw.reddit.Submission] = list(redditor.submissions.new(limit=100))

            for post_id, content in posts.items():
                best_match: Optional[praw.reddit.Submission] = None
                highest_similarity: float = 0.0
                best_link: str = ""

                for submission in reddit_posts:
                    similarity: float = SequenceMatcher(None, content, submission.title).ratio()
                    if similarity > highest_similarity:
                        highest_similarity = similarity
                        best_match = submission
                        best_link = f"https://reddit.com{submission.permalink}"

                if best_match:
                    connected_posts[post_id] = best_link

            cls.logger.info(f"Connected posts to Reddit: {connected_posts}")
            cls._save_connections(connected_posts)

            return connected_posts

        except DBConnectionException as e:
            cls.logger.error(f"Failed to connect posts to Reddit: {e}")
            raise RedditPostConnectionException(f"Failed to save connections: {e}") from e

        except Exception as e:
            cls.logger.error(f"Failed to connect posts to Reddit: {e} \n{traceback.format_exc()}")
            raise RedditPostConnectionException(f"Failed to connect posts to Reddit: {e}") from e

    @classmethod
    def _save_connections(cls, connections: Dict[str, str]) -> None:
        """
        Save the connections to the database.

        Args:
            connections (Dict[str, str]): The connections to save.

        Raises:
            DBConnectionException: If the database connection fails.
        """
        try:
            collection_archive: Collection = cls._db_connection.get_collection("post_archive")

            for post_id, link in connections.items():
                collection_archive.update_one({"_id": ObjectId(post_id)}, {"$set": {"redditLink": link}})

        except DBConnectionException:
            cls.logger.error("DB connection error.")
            raise DBConnectionException("Could not connect to the database while saving connections.")

        except Exception as e:
            cls.logger.error(f"An error occurred while saving connections: {e} \n{traceback.format_exc()}")

        finally:
            cls._db_connection.close_connection()
