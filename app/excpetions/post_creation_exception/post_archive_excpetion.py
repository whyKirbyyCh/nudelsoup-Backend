

class PostArchiveException(Exception):
    """ Exception raised when an error occurs while archiving the posts """

    def __init__(self, message: str) -> None:
        """
        Initialize the PostArchiveException with the message to be displayed.

        Args:
            message (str): The message to be displayed.

        Returns:
            None

        Raises:
            None
        """
        super().__init__(message)