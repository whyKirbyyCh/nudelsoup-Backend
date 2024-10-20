

class UserLimitsException(Exception):
    def __init__(self, message: str) -> None:
        """
        Initialize the UserLimitsException with the message to be displayed.

        Args:
            message (str): The message to be displayed.
        """
        super().__init__(message)
