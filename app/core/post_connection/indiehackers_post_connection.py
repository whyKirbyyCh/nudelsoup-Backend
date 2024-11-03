import time
import re
from app.db.db_connection import DBConnection
from app.config.logger_config import Logger
from app.config.scraper_config import Scraper
from dotenv import load_dotenv
from typing import Dict, Tuple
from app.excpetions.post_connection_exception.indiehackers_post_connection_exception import IndiehackersPostConnectionException
from app.excpetions.config.scraper_exception import ScraperException
from app.services.post_connection.indiehackers_user_site_retrival_service import IndiehackersUserSiteRetrivalService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import traceback
from difflib import SequenceMatcher
from bs4 import BeautifulSoup
from app.excpetions.db.db_connection_exception import DBConnectionException
from pymongo.collection import Collection
from bson import ObjectId


class IndiehackersPostConnection:
    """ A class connecting a post to Indiehackers. """

    logger = Logger.get_logger()
    scraper = Scraper.get_scraper()
    load_dotenv(override=True)
    _db_connection: DBConnection = DBConnection()

    @classmethod
    def connect_posts_to_indiehackers(cls, post: Tuple[str, str], user_id: str) -> Dict[str, str]:
        """
        Connect posts to Indiehackers by finding the most similar post for each content entry.

        Args:
            post (Tuple[str, str]): The dictionary of posts to connect.
            user_id (str): The ID of the user.

        Returns:
            Dict[str, str]: A dictionary with post_id as keys and the Indiehackers link as values.

        Raises:
            IndiehackersPostConnectionException: If an error occurs while connecting the posts to Indiehackers.
            ScraperException: If an error occurs while connecting the posts to Indiehackers.
        """
        connected_posts: Dict[str, str] = {}

        try:
            url: str = IndiehackersUserSiteRetrivalService.get_user_site(user_id) + "/history"

            cls.scraper.get(url)
            cls.scraper.implicitly_wait(10)

            outer_section = cls.scraper.find_element(By.XPATH, "//section[@id='ember42' and contains(@class, 'user-feed')]")
            options_div = outer_section.find_element(By.CLASS_NAME, "user-feed__options")
            comments_feed = options_div.find_element(By.XPATH, ".//li[contains(@class, 'user-feed__option') and contains(@class, 'user-feed__option--selected') and .//span[text()='Comments']]")
            comments_feed.click()

            cls.scraper.sleep(5)

            user_feed_section = cls.scraper.find_element(By.CSS_SELECTOR, "section.user-feed.ember-view")
            user_posts = user_feed_section.find_elements(By.CSS_SELECTOR, "div.user-feed__item.user-feed-item.user-feed-item--post.ember-view")[:10]

            most_similar_post = None
            max_similarity = 0
            date_pattern = r"^\w{3} \d{1,2} \d{4} created a post called "

            for user_post in user_posts:
                post_html = user_post.get_attribute("outerHTML")
                soup = BeautifulSoup(post_html, "html.parser")
                post_text = soup.get_text(strip=True)
                post_text = re.sub(date_pattern, "", post_text)
                post_text = re.sub(r"\s+", " ", post_text).lower().strip()

                main_text = re.sub(r"\s+", " ", post[1]).lower().strip()

                similarity = SequenceMatcher(None, main_text, post_text).ratio()

                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_post = user_post

            if most_similar_post:
                post_link_element = most_similar_post.find_element(By.CSS_SELECTOR, "a.ember-view")
                post_link = post_link_element.get_attribute("href")
                connected_posts[post[0]] = post_link

            # cls._save_connections(connected_posts)
            cls.logger.info(f"Connected posts to Indiehackers: {connected_posts}")
            return connected_posts

        except ScraperException as e:
            cls.logger.error(f"An unknown error happened during scraping: {e} \n{traceback.format_exc()}")
            raise IndiehackersPostConnectionException(f"An unknown error happened during scraping: {e}")

        except NoSuchElementException as e:
            cls.logger.error(f"An element was not found: {e} \n{traceback.format_exc()}")
            raise IndiehackersPostConnectionException(f"An element was not found: {e} \n{traceback.format_exc()}")

        except TimeoutException as e:
            cls.logger.error(f"An error occurred while connecting posts to Indiehackers: {e} \n{traceback.format_exc()}")
            raise IndiehackersPostConnectionException(f"An error occurred while connecting posts to Indiehackers: {e}")

        except Exception as e:
            cls.logger.error(f"An error occurred while connecting posts to Indiehackers: {e} \n{traceback.format_exc()}")
            raise IndiehackersPostConnectionException(f"An error occurred while connecting posts to Indiehackers: {e}")

        finally:
            cls.scraper.quit()

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
                collection_archive.update_one({"_id": ObjectId(post_id)}, {"$set": {"indiehackersLink": link}})

        except DBConnectionException:
            cls.logger.error("DB connection error.")
            raise DBConnectionException("Could not connect to the database while saving connections.")

        except Exception as e:
            cls.logger.error(f"An error occurred while saving connections: {e} \n{traceback.format_exc()}")
            raise IndiehackersPostConnectionException(f"An unknown error occurred while saving connections: {e}")

        finally:
            cls._db_connection.close_connection()


if __name__ == "__main__":
    try:
        res = IndiehackersPostConnection.connect_posts_to_indiehackers(user_id="", post=("id", """We are live on Product Hunt with Synth Resume – an AI-powered job-specific resume generator for professionals.

Check it out and let us know what you think, we’d love your feedback!"""))

        print(res)

    except Exception as ey:
        print(f"An error occurred while connecting posts to Indiehackers: {ey} \n{traceback.format_exc()}")
