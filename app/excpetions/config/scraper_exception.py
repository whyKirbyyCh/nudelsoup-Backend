

class ScraperException(Exception):
    """ A base class for all scraper exceptions. """

    def __init__(self, message: str) -> None:
        """
        Initialize the ScraperException with a message.

        Args:
            message (str): The message to be displayed.
        """

        super().__init__(message)