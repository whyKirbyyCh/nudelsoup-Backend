

class PasswordFormatValidationException(Exception):
    """Class to handle password format validation errors."""

    def __init__(self, message: str) -> None:
        """
        Initialize the PasswordFormatValidationException with the message to be displayed.

        Args:
            message (str): The message to be displayed.

        Returns:
            None

        Raises:
            None
        """
        super().__init__(message)
