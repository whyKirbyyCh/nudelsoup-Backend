from seleniumbase import Driver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
from app.config.logger_config import Logger
from app.excpetions.config.scraper_exception import ScraperException


class Scraper:
    """Class to configure and initialize a web scraper using undetected Chrome browser."""

    logger = Logger().get_logger()

    @classmethod
    def get_scraper(cls) -> Driver:
        """
        Returns a configured undetected Chrome WebDriver instance.

        Returns:
            Driver: An instance of SeleniumBase Chrome WebDriver.

        Raises:
            ScraperException: If the CHROME_PATH environment variable is not set.
        """
        try:
            load_dotenv(override=True)

            chrome_path = os.getenv("CHROME_PATH")
            if not chrome_path:
                raise ScraperException("CHROME_PATH environment variable is not set.")

            options = Options()
            options.binary_location = chrome_path
            options.add_argument("--disable-blink-features=AutomationControlled")

            driver = Driver(uc=True, headless=False)
            driver.driver_options = options

            return driver

        except ScraperException as e:
            cls.logger.exception(f"An error occurred while configuring the scraper: {e}")
            raise ScraperException(f"An error occurred while configuring the scraper: {e}")

        except Exception as e:
            cls.logger.exception(f"An unexpected error occurred while configuring the scraper: {e}")
            raise ScraperException(f"An unexpected error occurred while configuring the scraper: {e}")
