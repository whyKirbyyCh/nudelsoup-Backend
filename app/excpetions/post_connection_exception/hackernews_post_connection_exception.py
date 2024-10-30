

class HackernewsPostConnectionException(Exception):
    """ Exception class for Hackernews post connection. """

    def __init__(self, message: str) -> None:
        """
        Initialize the HackernewsPostConnectionException with a message.

        Args:
            message (str): The message to be displayed.
        """
        super().__init__(message)
