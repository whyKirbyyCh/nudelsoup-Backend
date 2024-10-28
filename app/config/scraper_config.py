import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
from app.config.logger_config import Logger
from app.excpetions.config.scraper_exception import ScraperException


class Scraper:
    """Class to configure and initialize a web scraper using undetected Chrome browser."""

    logger = Logger().get_logger()

    @classmethod
    def get_scraper(cls) -> uc.Chrome:
        """
        Returns a configured undetected Chrome WebDriver instance.

        Returns:
            uc.Chrome: An instance of undetected Chrome WebDriver.

        Raises:
            ScraperException: If the CHROME_PATH environment variable is not set.
        """
        try:
            load_dotenv(override=True)

            chrome_path = os.getenv("CHROME_PATH")

            options = Options()
            options.headless = False

            if chrome_path:
                options.binary_location = chrome_path

            else:
                raise ScraperException("CHROME_PATH environment variable is not set.")

            options.add_argument("--disable-blink-features=AutomationControlled")

            driver = uc.Chrome(options=options)
            driver.implicitly_wait(5)

            return driver

        except ScraperException as e:
            cls.logger.exception(f"An error occurred while configuring the scraper: {e}")
            raise ScraperException(f"An error occurred while configuring the scraper: {e}")

        except Exception as e:
            cls.logger.exception(f"An error occurred while configuring the scraper: {e}")
            raise ScraperException(f"An error occurred while configuring the scraper: {e}")