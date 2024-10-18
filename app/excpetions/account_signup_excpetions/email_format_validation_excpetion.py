

class EmailFormatValidationException(Exception):
    """Exception raised when the email format check is not working as expected."""

    def __init__(self, message: str) -> None:
        """
        Initialize the EmailFormatValidationException with the email that caused the exception.

        Args:
            message (str): The message to be displayed.

        Returns:
            None

        Raises:
            None
        """
        super().__init__(message)
        