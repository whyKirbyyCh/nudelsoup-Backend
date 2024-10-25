

class RedditPostAnalyticsException(Exception):
    """ Exception class for Reddit post analytics. """

    def __init__(self, message: str) -> None:
        """
        Initialize the RedditPostAnalyticsException with a message.

        Args:
            message (str): The message to be displayed.
        """
        super().__init__(message)