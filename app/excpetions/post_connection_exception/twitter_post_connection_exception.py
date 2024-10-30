

class TwitterPostConnectionException(Exception):
    """ Twitter post connection exception. """

    def __init__(self, message: str) -> None:
        """
        Initialize the TwitterPostConnectionException with a message.

        Args:
            message (str): The message to be displayed.
        """
        super().__init__(message)
