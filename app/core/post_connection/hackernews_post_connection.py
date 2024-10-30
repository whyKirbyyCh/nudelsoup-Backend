import traceback
from typing import Dict, Tuple
from app.services.post_connection.hackernews_user_site_retrival_service import HackernewsUserSiteRetrivalService
from app.excpetions.post_connection_exception.hackernews_post_connection_exception import HackernewsPostConnectionException
from app.config.scraper_config import Scraper
from app.excpetions.config.scraper_exception import ScraperException
from app.config.logger_config import Logger
from app.db.db_connection import DBConnection
from app.excpetions.db.db_connection_exception import DBConnectionException
from difflib import SequenceMatcher
from bs4 import BeautifulSoup
from app.excpetions.db.db_connection_exception import DBConnectionException
from pymongo.collection import Collection
from bson import ObjectId
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class HackernewsPostConnection:
    """ A class for connecting a post to Hackernews. """

    logger = Logger.get_logger()
    scraper = Scraper.get_scraper()
    _db_connection: DBConnection = DBConnection()

    @classmethod
    def get_user_site(cls, post: Tuple[str, str], user_id: str) -> Dict[str, str]:
        """
        Connect posts to Hackernews by finding the most similar Hackernews post for each content entry.

        Args:
            post (Tuple[str, str]): The dictionary of posts to connect.
            user_id (str): The ID of the user.

        Returns:
            Dict[str, str]: A dictionary with post_id as keys and the Hackernews link as values.

        Raises:
            HackernewsPostConnectionException: If an error occurs while connecting the posts to Hackernews.
        """
        connected_posts: Dict[str, str] = {}
        
        try:
            url: str = HackernewsUserSiteRetrivalService.get_user_site(user_id)

            cls.scraper.get(url)
            cls.scraper.implicitly_wait(10)

            elements: list = cls.scraper.find_elements(By.CSS_SELECTOR, "tr.athing")[:10]

            if not elements:
                raise HackernewsPostConnectionException("No posts found")

            most_similar_post = None
            max_similarity = 0

            for element in elements:
                title_element = element.find_element(By.CSS_SELECTOR, "td.title > span.titleline")
                link_element = title_element.find_element(By.TAG_NAME, "a")

                cls.logger.info(f"{link_element}")

                cls.logger.info(f"{link_element.text}")

                similarity = SequenceMatcher(None, post[1], link_element.text).ratio()

                cls.logger.info(f"Similarity: {similarity}")

                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_post = element

            link_id = most_similar_post.get_attribute("id")
            link = f"https://news.ycombinator.com/item?id={link_id}"
            
            connected_posts[post[0]] = link
            
            return connected_posts

        except ScraperException as e:
            cls.logger.error(f"An unknown error happened during scraping: {e} \n{traceback.format_exc()}")
            raise HackernewsPostConnectionException(f"An unknown error happened during scraping: {e}")

        except NoSuchElementException as e:
            cls.logger.error(f"An element was not found: {e} \n{traceback.format_exc()}")
            raise HackernewsPostConnectionException(f"An element was not found: {e} \n{traceback.format_exc()}")

        except TimeoutException as e:
            cls.logger.error(
                f"An error occurred while connecting posts to Hackernews: {e} \n{traceback.format_exc()}")
            raise HackernewsPostConnectionException(f"An error occurred while connecting posts to Hackernews: {e}")

        except Exception as e:
            cls.logger.error(
                f"An error occurred while connecting posts to Hackernews: {e} \n{traceback.format_exc()}")
            raise HackernewsPostConnectionException(f"An error occurred while connecting posts to Hackernews: {e}")

        finally:
            cls.scraper.quit()


if __name__ == "__main__":
    try:
        res = HackernewsPostConnection.get_user_site(("id", "Writing in Pictures: Richard Scarry and the art of children's literature"), "test")

        print(res)

    except Exception as ey:
        print(f"An error occurred while connecting posts to Hackernews: {ey} \n{traceback.format_exc()}")

