

class RedditSignupException(Exception):
    """ A class that is used to represent an exception that occurs while signing up a user on Reddit. """
    def __init__(self, message: str) -> None:
        """
        Initializes the class with a message.

        Args:
            message (str): The message to be displayed.
        """
        super().__init__(message)
