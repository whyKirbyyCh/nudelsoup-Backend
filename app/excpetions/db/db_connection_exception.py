

class DBConnectionException(Exception):
    """
    Exception raised when there is an error with the DBConnection class.
    """

    def __init__(self, message: str) -> None:
        """
        Initializes the DBConnectionException class.

        Args:
            message (str): The error message.
        """
        super().__init__(message)