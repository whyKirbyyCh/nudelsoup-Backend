from typing import Dict, Tuple
from app.config.logger_config import Logger
import traceback
from app.excpetions.post_connection_exception.post_connection_exception import PostConnectionException
from app.excpetions.post_connection_exception.reddit_post_connection_exception import RedditPostConnectionException
from app.excpetions.post_connection_exception.twitter_post_connection_exception import TwitterPostConnectionException
from app.excpetions.post_connection_exception.hackernews_post_connection_exception import HackernewsPostConnectionException
from app.excpetions.post_connection_exception.linkedin_post_connection_excpetion import LinkedinPostConnectionException
from app.excpetions.post_connection_exception.indiehackers_post_connection_exception import IndiehackersPostConnectionException
from app.excpetions.db.db_connection_exception import DBConnectionException
from app.core.post_connection.reddit_post_connection import RedditPostConnection
from app.core.post_connection.linkedin_post_connection import LinkedInPostConnection
from app.core.post_connection.indiehackers_post_connection import IndiehackersPostConnection
from app.core.post_connection.hackernews_post_connection import HackernewsPostConnection
from app.core.post_connection.twitter_post_connection import TwitterPostConnection
from app.db.db_connection import DBConnection
from pymongo.collection import Collection
from bson import ObjectId


class PostConnectionManager:
    """ Post connection manager class. """

    def __init__(self, posts: Dict[str, Tuple[str, str]], user_id: str) -> None:
        """
        Initializes the PostConnectionManager class.

        Args:
            self
            posts (Dict[str, Dict[str, str]]): The posts to connect.
            user_id (str): The user ID.
        """
        self.posts: Dict[str, Tuple[str, str]] = posts
        self.user_id: str = user_id

        self.logger = Logger.get_logger()
        self._db_connection: DBConnection = DBConnection()
        self.connected_posts: Dict[str, str] = {}

    def connect_posts(self) -> Dict[str, str]:
        """
        Handles all the different post connections.

        Raises:
            PostConnectionException: If an error occurs while connecting the posts.
        """
        try:
            for site, content in self.posts.items():
                try:
                    if site.lower().strip() == "reddit":
                        self.connected_posts.update(RedditPostConnection.connect_posts_to_reddit(posts=content, user_id=self.user_id))
                        self.logger.info(f"Connected {self.connected_posts}")

                    elif site.lower().strip() == "linkedin":
                        self.connected_posts.update(LinkedInPostConnection.connect_posts_to_linkedin(post=content, user_id=self.user_id))
                        self.logger.info(f"Connected {self.connected_posts}")

                    elif site.lower().strip() == "indiehackers":
                        self.connected_posts.update(IndiehackersPostConnection.connect_posts_to_indiehackers(post=content, user_id=self.user_id))
                        self.logger.info(f"Connected {self.connected_posts}")

                    elif site.lower().strip() == "hackernews":
                        self.connected_posts.update(HackernewsPostConnection.connect_posts_to_hackernews(post=content, user_id=self.user_id))
                        self.logger.info(f"Connected {self.connected_posts}")

                    elif site.lower().strip() == "twitter":
                        self.connected_posts.update(TwitterPostConnection.connect_posts_to_twitter(post=content, user_id=self.user_id))
                        self.logger.info(f"Connected {self.connected_posts}")

                    else:
                        continue

                except (RedditPostConnectionException, IndiehackersPostConnectionException, TwitterPostConnectionException, LinkedinPostConnectionException, HackernewsPostConnectionException) as e:
                    self.logger.error(f"An error occurred while connecting the posts to Reddit: {e} \n{traceback.format_exc()}")
                    continue

                except Exception as e:
                    self.logger.error(f"An error occurred while connecting the posts: {e} \n{traceback.format_exc()}")
                    raise PostConnectionException(f"An error occurred while connecting the posts: {e}")

            self.logger.info(f"Connected posts: {self.connected_posts}")

            # self._copy_connected_to_live_posts()

            return {post_tuple[0]: post_tuple[0] in self.connected_posts for post_tuple in self.posts.values()}

        except PostConnectionException as e:
            self.logger.error(f"An error occurred while connecting the posts: {e} \n{traceback.format_exc()}")
            raise PostConnectionException(f"An error occurred while connecting the posts: {e}")

        except Exception as e:
            self.logger.error(f"An error occurred while connecting the posts: {e} \n{traceback.format_exc()}")
            raise PostConnectionException(f"An error occurred while connecting the posts: {e}")

    def _copy_connected_to_live_posts(self) -> None:
        """
        Copy the connected posts from the archive posts to the live posts.

        Args:
            self.connected_posts (Dict[str, Dict[str, str]]): The connected posts.

        Raises:
            PostConnectionException: If an error occurs while copying the connected posts.
            DBConnectionException: If an error occurs while copying the connected posts.
        """
        try:
            post_archive: Collection = self._db_connection.get_collection(collection_name="post_archive")
            post_live: Collection = self._db_connection.get_collection(collection_name="post_live")

            for post_id, link in self.connected_posts.items():
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


if __name__ == "__main__":
    postss = {"hackernews": ("id1", "Writing in Pictures: Richard Scarry and the art of children's literature"),
              "indiehackers": ("id2", """We are live on Product Hunt with Synth Resume – an AI-powered job-specific resume generator for professionals. Check it out and let us know what you think, we’d love your feedback!"""),
              "linkedin": ("id3", "Want to sample more of our journalism before subscribing? Register here to access free FT articles: https://lnkd.in/e4U2_erE"),
              "twitter": ("id4", """I sure make the dumbest faces while playing ultimate"""),
              }
    try:
        connection_manager: PostConnectionManager = PostConnectionManager(posts=postss, user_id="test")

        connection_manager.connect_posts()

    except PostConnectionException as es:
        print(es)
