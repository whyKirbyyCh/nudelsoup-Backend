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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


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

            posts_collected = 0
            scroll_attempts = 0
            max_scroll_attempts = 10  # Define a max to prevent infinite loops if the page has no more posts

            while posts_collected < 10 and scroll_attempts < max_scroll_attempts:
                # Locate all post elements in the main feed section
                content_container = cls.scraper.find_element(By.CLASS_NAME, "scaffold-finite-scroll__content")
                post_elements = content_container.find_elements(By.CSS_SELECTOR, "div.ember-view.occludable-update")

                # Process each post in the current viewport
                for post in post_elements:
                    try:
                        # Extract post content
                        post_content_element = post.find_element(By.CSS_SELECTOR,
                                                                 "div.update-components-text.relative.update-components-update-v2__commentary")
                        post_content = post_content_element.text
                        cls.logger.info(f"Post content: {post_content}")

                        post_id = post.get_attribute("id")
                        connected_posts[post_id] = post_content
                        posts_collected += 1

                    except Exception as e:
                        cls.logger.warning(f"Could not extract content from post {post.get_attribute('id')}")

                cls.scraper.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                time.sleep(4)  # Allow time for new posts to load

                # Update attempt count if no new posts load
                new_post_elements = content_container.find_elements(By.CSS_SELECTOR, "div.ember-view.occludable-update")
                if len(new_post_elements) == len(post_elements):
                    scroll_attempts += 1  # Increment if no new posts were loaded
                else:
                    scroll_attempts = 0  # Reset if new posts loaded

            return connected_posts

        except ScraperException as e:
            cls.logger.error(f"An error occurred while connecting to LinkedIn: {e} \n{traceback.format_exc()}")
            raise LinkedinPostConnectionException(f"An error occurred while connecting to LinkedIn: {e}")

        except Exception as e:
            cls.logger.error(f"An error occurred while connecting the posts to LinkedIn: {e} \n{traceback.format_exc()}")
            raise LinkedinPostConnectionException(f"An error occurred while connecting the posts to LinkedIn: {e}")


if __name__ == "__main__":
    try:
        linkedin_connection = LinkedInPostConnection()
        result = linkedin_connection.connect_posts_to_linkedin(
            posts={"post1": "content1", "post2": "content2", "post3": "content3"},
            user_id="user_id"
        )
    except Exception as se:
        print(f"Error: {se}")
