

class LinkedinPostConnectionException(Exception):
    """ Exception class for LinkedIn post connection. """
    def __init__(self, message: str) -> None:
        """
        Initialize the LinkedInPostConnectionException with a message.

        Args:
            message (str): The message to be displayed.
        """
        super().__init__(message)
