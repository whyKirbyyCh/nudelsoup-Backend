import praw
from app.config.logger_config import Logger
from dotenv import load_dotenv
from typing import List, Dict, Union, Tuple
from app.excpetions.analytics_exception.reddit_post_analytics_exception import RedditPostAnalyticsException
import os


class RedditPostAnalyticsRetrival:
    """ Class to retrieve post analytics from Reddit. """

    logger = Logger.get_logger()
    load_dotenv(override=True)

    @classmethod
    def get_post_analytics(cls, posts: List[str]) -> Dict[str, Union[int, str, List[str]]]:
        """ Get post analytics from Reddit. """

        results: Dict[str, Union[int, str, List[str]]] = {}

        try:
            urls: List[str] = cls._get_posts_urls(posts)

            reddit: praw.Reddit = praw.Reddit(
                                    client_id=os.getenv("REDDIT_CLIENT_ID"),
                                    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                                    user_agent=os.getenv("REDDIT_USER_AGENT")
                                  )

            for post_id, url in urls:
                submission: praw.reddit.Submission = reddit.submission(url=url)

                results[post_id] = {
                    "title": submission.title,
                    "content": submission.selftext,
                    "upvotes": submission.score,
                    "num_comments": submission.num_comments,
                    "comments": [comment.body for comment in submission.comments.list()]
                }

            return results

        except Exception as e:
            cls.logger.error(f"Failed to get post analytics: {e}")
            raise RedditPostAnalyticsException(f"Failed to get post analytics: {e}")

    @classmethod
    def _get_posts_urls(cls, posts: List) -> List[Tuple[str, str]]:
        """ Get posts urls from Reddit. """
        pass
