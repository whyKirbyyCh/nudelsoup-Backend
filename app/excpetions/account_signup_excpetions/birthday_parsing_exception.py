

class BirthdayParsingException(Exception):
    """Class that is used to represent an exception that occurs while transforming a birthday string into a Birthday object."""

    def __init__(self, message: str) -> None:
        """
        Initializes the class with a message.

        Args:
            message (str): The message to be displayed.

        Returns:
            None

        Raises:
            None
        """
        super().__init__(message)
