

class OpenAICompletionException(Exception):
    """
    Exception class for OpenAI completion exceptions.
    """
    def __init__(self, message: str) -> None:
        """
        Initialize the OpenAICompletionException with the message to be displayed.

        Args:
            message (str): The message to be displayed.

        Returns:
            None

        Raises:
            None
        """
        super().__init__(message)
