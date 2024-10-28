

class PostConnectionException(Exception):
    """ Base class for all post connection exceptions. """

    def __init__(self, message: str) -> None:
        """
        Initialize the PostConnectionException with a message.

        Args:
            message (str): The message to be displayed.
        """
        super().__init__(message)
