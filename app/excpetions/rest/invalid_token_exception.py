

class InvalidTokenException(Exception):
    """ Invalid token exception. """
    def __init__(self, message: str) -> None:
        """
        Initialize the InvalidTokenException with a message.

        Args:
            message (str): The message to be displayed.
        """
        super().__init__(message)