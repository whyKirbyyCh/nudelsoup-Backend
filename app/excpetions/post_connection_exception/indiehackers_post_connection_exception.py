

class IndiehackersPostConnectionException(Exception):
    """ Indiehackers post connection exception. """

    def __init__(self, message: str) -> None:
        """
        Initialize the IndiehackersPostConnectionException with a message.

        Args:
            message (str): The message to be displayed.
        """
        super().__init__(message)
