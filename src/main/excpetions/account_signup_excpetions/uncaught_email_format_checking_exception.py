

class UncaughtEmailFormatCheckingException(Exception):
    """Exception raised when an email format checking exception is not caught."""

    def __init__(self, message: str) -> None:
        """
        Initialize the UncaughtEmailFormatCheckingException with the email that caused the exception.

        Args:
            message (str): The message to be displayed.

        Returns:
            None

        Raises:
            None
        """
        super().__init__(message)