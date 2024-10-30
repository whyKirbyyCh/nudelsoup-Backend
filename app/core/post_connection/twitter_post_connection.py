import time
from app.services.post_connection.twitter_user_site_retrival_service import TwitterUserSiteRetrivalService
from app.config.logger_config import Logger
from app.config.scraper_config import Scraper
from app.db.db_connection import DBConnection
from dotenv import load_dotenv
from typing import Tuple, Dict, Optional
from app.excpetions.post_connection_exception.twitter_post_connection_exception import TwitterPostConnectionException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from difflib import SequenceMatcher
import re


class TwitterPostConnection:
    """ A class connecting a post to Twitter. """

    logger = Logger.get_logger()
    scraper = Scraper.get_scraper()
    _db_connection: DBConnection = DBConnection()
    load_dotenv(override=True)

    @classmethod
    def connect_posts_to_twitter(cls, post: Tuple[str, str], user_id: str) -> Dict[str, str]:
        """ Connect posts to Twitter by finding the most similar Twitter post for each content entry.

        Args:
            post (Tuple[str, str]): The dictionary of posts to connect.
            user_id (str): The ID of the user.

        Returns:
            Dict[str, str]: A dictionary with post_id as keys and the Twitter link as values.

        Raises:
            TwitterPostConnectionException: If an error occurs while connecting the posts to Twitter.
            ScraperException: If an error occurs while connecting the posts to Twitter.
        """
        connected_posts: Dict[str, str] = {}
        try:
            cls._login_twitter()

            time.sleep(5)

            url: str = TwitterUserSiteRetrivalService.get_user_site(user_id)
            cls.scraper.get(url)
            cls.scraper.implicitly_wait(10)

            main_feed = WebDriverWait(cls.scraper, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "div.css-175oi2r.r-kemksi.r-1kqtdi0.r-1ua6aaf.r-th6na.r-1phboty.r-16y2uox.r-184en5c.r-1abdc3e.r-1lg4w6u.r-f8sm7e.r-13qz1uu.r-1ye8kvj"))
            )
            posts_column = main_feed.find_element(By.CSS_SELECTOR, "section[role='region'].css-175oi2r")

            elements = posts_column.find_elements(By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")[:10]
            cls.logger.info(f"Elements: {len(elements)}")

            most_similar_post: Optional[str] = None
            max_similarity: float = 0

            for element in elements:
                try:
                    inner_div = element.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-18u37iz.r-1q142lx")
                    link_element = inner_div.find_element(By.CSS_SELECTOR, "a[role='link']")
                    link = link_element.get_attribute("href")

                    container_div = element.find_element(By.CSS_SELECTOR, "div[data-testid='tweetText']")
                    text_element = container_div.find_element(By.CSS_SELECTOR, "span.css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3")
                    text = text_element.text.replace("\n", "").strip().lower()

                    main_text = re.sub(r"\s+", " ", post[1]).lower().strip()

                    similarity = SequenceMatcher(None, main_text, text).ratio()
                    if similarity > max_similarity:
                        max_similarity = similarity
                        most_similar_post = link

                except TimeoutException as e:
                    continue

                except NoSuchElementException as e:
                    continue

                except Exception as e:
                    continue

            connected_posts[post[0]] = most_similar_post
            return connected_posts

        except TimeoutException as e:
            cls.logger.error(f"Timeout error while connecting posts to Twitter: {e}")
            raise TwitterPostConnectionException("Timeout error while connecting posts to Twitter")

        except NoSuchElementException as e:
            cls.logger.error(f"No such element error while connecting posts to Twitter: {e}")
            raise TwitterPostConnectionException("No such element error while connecting posts to Twitter")

        except TwitterPostConnectionException as e:
            cls.logger.error(f"TwitterPostConnectionException error while connecting posts to Twitter: {e}")
            raise TwitterPostConnectionException(f"TwitterPostConnectionException error while connecting posts to Twitter: {e}")

        except Exception as e:
            cls.logger.error(f"An error occurred while connecting the posts to Twitter: {e}")
            raise TwitterPostConnectionException(f"An error occurred while connecting the posts to Twitter: {e}")

    @classmethod
    def _login_twitter(cls):
        """
        Login to Twitter.

        Raises:
            TwitterPostConnectionException: If an error occurs while logging in to Twitter.
        """
        try:
            cls.scraper.get("https://x.com/login")
            cls.scraper.implicitly_wait(10)

            username_field = WebDriverWait(cls.scraper, 10).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, "input[name='text'][autocomplete='username']"))
            )
            username_field.send_keys(os.getenv("TWITTER_CLIENT_ID"))

            next_button = WebDriverWait(cls.scraper, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR,
                                            "button[role='button'].css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-ywje51.r-184id4b.r-13qz1uu.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l"))
            )
            next_button.click()
            cls.scraper.implicitly_wait(10)

            try:
                error_message = WebDriverWait(cls.scraper, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, "span.css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3"))
                )

            except TimeoutException:
                error_message = None

            if error_message:
                username_field = WebDriverWait(cls.scraper, 10).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, "input[data-testid='ocfEnterTextTextInput']"))
                )
                username_field.send_keys(os.getenv("TWITTER_CLIENT_USERNAME"))

                next_button = WebDriverWait(cls.scraper, 10).until(
                    ec.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='ocfEnterTextNextButton']"))
                )
                next_button.click()
                cls.scraper.implicitly_wait(10)

                password_field = WebDriverWait(cls.scraper, 10).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
                )
                password_field.send_keys(os.getenv("TWITTER_CLIENT_SECRET"))

                login_button = WebDriverWait(cls.scraper, 10).until(
                    ec.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='LoginForm_Login_Button']"))
                )
                login_button.click()
                cls.scraper.implicitly_wait(10)

            else:
                password_field = WebDriverWait(cls.scraper, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, "div.css-175oi2r input[type='password']"))
                )
                password_field.send_keys(os.getenv("TWITTER_CLIENT_SECRET"))

                login_button = WebDriverWait(cls.scraper, 10).until(
                    ec.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='LoginForm_Login_Button']"))
                )
                login_button.click()

        except TimeoutException as e:
            cls.logger.error(f"Timeout error while logging in to Twitter: {e}")
            raise TwitterPostConnectionException("Timeout error while logging in to Twitter")

        except NoSuchElementException as e:
            cls.logger.error(f"No such element error while logging in to Twitter: {e}")
            raise TwitterPostConnectionException("No such element error while logging in to Twitter")

        except TwitterPostConnectionException as e:
            cls.logger.error(f"An error occurred while logging in to Twitter: {e}")
            raise TwitterPostConnectionException(f"An error occurred while logging in to Twitter: {e}")

        except Exception as e:
            cls.logger.error(f"An error occurred while logging in to Twitter: {e}")
            raise TwitterPostConnectionException(f"An error occurred while logging in to Twitter: {e}")


if __name__ == "__main__":
    x = TwitterPostConnection.connect_posts_to_twitter(("test", """The Macbook Pro gets its M4 update

The entire Mac lineup now starts with 16GB of memory

(I'm still on my M1 Max and doing just fine, but this is the first one I've been tempted by)"""), "test")

    print(x)
