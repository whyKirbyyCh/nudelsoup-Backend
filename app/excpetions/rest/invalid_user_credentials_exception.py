

class InvalidUserCredentialsException(Exception):
    """ Invalid user credentials exception."""
    def __init__(self, message: str) -> None:
        """
        Initialize the InvalidUserCredentialsException with a message.

        Args:
            message (str): The message to be displayed.
        """
        super().__init__(message)
