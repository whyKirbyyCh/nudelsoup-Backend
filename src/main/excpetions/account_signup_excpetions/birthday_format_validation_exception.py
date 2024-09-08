

class BirthdayFormatValidationException(Exception):
    """Exception to be raised when the birthday format check is not working."""

    def __init__(self, message: str):
        """
        Initialize the BirthdayFormatValidationException with the message to be displayed.

        Args:
            message (str): The message to be displayed.

        Returns:
            None

        Raises:
            None
        """
        super().__init__(message)