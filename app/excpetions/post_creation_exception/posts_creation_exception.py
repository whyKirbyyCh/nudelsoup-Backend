

class PostsCreationException(Exception):
    """ Exception class for posts creation exceptions. """
    def __init__(self, message: str) -> None:
        """
        Initialize the PostsCreationException with the message to be displayed.

        Args:
            message (str): The message to be displayed.

        Returns:
            None

        Raises:
            None
        """
        super().__init__(message)
