

class RedditPostConnectionException(Exception):
    """ Exception class for Reddit post connection. """

    def __init__(self, message: str) -> None:
        """
        Initialize the RedditPostConnectionException with a message.

        Args:
            message (str): The message to be displayed.
        """
        super().__init__(message)
