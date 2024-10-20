

class UserAuthenticationException(Exception):
    """
    Class that represents an exception that occurs during user authentication.
    """

    def __init__(self, message: str) -> None:
        """
        Initializes the UserAuthenticationException class.

        Args:
            message (str): The error message.
        """
        super().__init__(message)
