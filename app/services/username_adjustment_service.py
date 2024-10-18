

class UsernameAdjustmentService:
    """Class that is used to adjust the username."""

    def __init__(self, username: str) -> None:
        """
        Initializes the class with the username to be adjusted.

        Args:
            username (str): The username to be adjusted.

        Returns:
            None

        Raises:
            TypeError: If the username is not a string.
            ValueError: If the username is empty.
        """
        if not username:
            raise ValueError("username must not be empty")

        if not isinstance(username, str):
            raise TypeError("username must be a string")

        self.username = username
