from app.db.db_connection import DBConnection
from app.config.logger_config import Logger
from dotenv import load_dotenv
from typing import Dict
from app.config.scraper_config import Scraper
from app.excpetions.config.scraper_exception import ScraperException
from app.excpetions.post_connection_exception.linkedin_post_connection_excpetion import LinkedinPostConnectionException
import time
import traceback
from selenium.webdriver.common.by import By
import os
from app.services.post_connection.linkedin_user_site_retrival_service import LinkedinUserSiteRetrivalService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pyperclip


class LinkedInPostConnection:
    """ A class connecting the posts to LinkedIn. """

    logger = Logger.get_logger()
    scraper = Scraper.get_scraper()
    load_dotenv(override=True)
    _db_connection: DBConnection = DBConnection()

    @classmethod
    def connect_posts_to_linkedin(cls, posts: Dict[str, str], user_id: str) -> Dict[str, str]:
        """
        Connect posts to LinkedIn by finding the most similar LinkedIn post for each content entry.

        Args:
            posts (Dict[str, str]): The dictionary of posts to connect.
            user_id (str): The ID of the user.

        Returns:
            Dict[str, str]: A dictionary with post_id as keys and the LinkedIn link as values.

        Raises:
            LinkedInPostConnectionException: If an error occurs while connecting the posts to LinkedIn.
            ScraperException: If an error occurs while connecting the posts to LinkedIn.
        """
        connected_posts: Dict[str, str] = {}

        try:
            cls.scraper.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
            time.sleep(5)

            email: str = os.getenv("LINKEDIN_CLIENT_ID")
            password: str = os.getenv("LINKEDIN_CLIENT_SECRET")

            username_field = cls.scraper.find_element(By.ID, "username")
            username_field.send_keys(email)

            password_field = cls.scraper.find_element(By.ID, "password")
            password_field.send_keys(password)

            sign_in_button = cls.scraper.find_element(
                By.CSS_SELECTOR,
                "button.btn__primary--large.from__button--floating[data-litms-control-urn='login-submit'][aria-label='Sign in'][type='submit']"
            )
            sign_in_button.click()

            time.sleep(5)

            user_link = LinkedinUserSiteRetrivalService.get_user_site()
            cls.scraper.get(user_link)

            time.sleep(5)

            sort_button = cls.scraper.find_element(By.ID, "sort-dropdown-trigger")
            sort_button.click()
            time.sleep(1)

            sort_container = cls.scraper.find_element(By.CSS_SELECTOR, "ul.sort-dropdown__list")
            recent_button = sort_container.find_element(By.XPATH, ".//button[.//span[text()='Recent']]")
            recent_button.click()

            time.sleep(5)

            sort_button.click()

            content_container = cls.scraper.find_element(By.CLASS_NAME, "scaffold-finite-scroll__content")
            post_elements = content_container.find_elements(By.CSS_SELECTOR, "div.ember-view.occludable-update")

            for post in post_elements[:1]:
                try:
                    text_element = post.find_element(By.CSS_SELECTOR, "div.feed-shared-inline-show-more-text span.break-words span[dir='ltr']")
                    text = text_element.text

                    cls.logger.info(f"Text: {text}")

                    post_menu_button = WebDriverWait(post, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.feed-shared-control-menu__trigger"))
                    )
                    post_menu_button.click()

                    time.sleep(4)

                    control_menu = WebDriverWait(cls.scraper, 10).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "feed-shared-control-menu__content"))
                    )

                    copy_link_button = WebDriverWait(control_menu, 10).until(
                        EC.element_to_be_clickable((By.XPATH, ".//h5[text()='Copy link to post']"))
                    )

                    copy_link_button.click()
                    time.sleep(1)

                    post_link = pyperclip.paste()

                except Exception as e:
                    cls.logger.error(f"An error occurred while finding the author link: {e} \n{traceback.format_exc()}")
                    continue

            return connected_posts

        except ScraperException as e:
            cls.logger.error(f"An error occurred while connecting to LinkedIn: {e} \n{traceback.format_exc()}")
            raise LinkedinPostConnectionException(f"An error occurred while connecting to LinkedIn: {e}")

        except Exception as e:
            cls.logger.error(f"An error occurred while connecting the posts to LinkedIn: {e} \n{traceback.format_exc()}")
            raise LinkedinPostConnectionException(f"An error occurred while connecting the posts to LinkedIn: {e}")

        finally:
            cls.scraper.quit()



if __name__ == "__main__":
    try:
        linkedin_connection = LinkedInPostConnection()
        result = linkedin_connection.connect_posts_to_linkedin(
            posts={"post1": "content1", "post2": "content2", "post3": "content3"},
            user_id="user_id"
        )
    except Exception as se:
        print(f"Error: {se}")
