import re

from src.main.excpetions.account_signup_excpetions.password_format_valdation_exception import PasswordFormatValidationException


class PasswordFormatChecker:
    """Class to check if a password has a valid format."""
    def __init__(self, password: str) -> None:
        """
        Initialize the PasswordFormatChecker with the password to be checked.

        Args:
            password (str): The password to be checked.

        Returns:
            None

        Raises:
            TypeError: If the password is not a string.
            ValueError: If the password is empty.
        """
        if not password:
            raise ValueError("password must not be empty")

        if not isinstance(password, str):
            raise TypeError("password must be a string")

        self.password = password

    def is_valid(self) -> bool:
        """
        Check if the password is valid.

        Args:

        Returns:
            bool: True if the password is valid, False otherwise.

        Raises:
            None
        """
        try:
            return self._is_valid_format()
        except PasswordFormatValidationException:
            return False

    def _is_valid_format(self) -> bool:
        """
        Check if the password has a valid format.

        Args:

        Returns:
            bool: True if the password has a valid format, False otherwise.

        Raises:
            PasswordFormatValidationException: If the password validation fails.
        """
        try:
            min_length: int = 8
            max_length: int = 20

            forbidden_characters: str = r'[äöÄÖßÿçåø|{}[\]~`!@#$%^&*()_+=\-<>;:\'",/\\\t\n\r\v\f\x00-\x1F\x7F]'

            has_upper: bool = re.search(r'[A-Z]', self.password) is not None
            has_lower: bool = re.search(r'[a-z]', self.password) is not None
            has_digit: bool = re.search(r'\d', self.password) is not None
            contains_forbidden_chars: bool = re.search(forbidden_characters, self.password) is not None

            if (min_length <= len(self.password) <= max_length and
                    has_upper and has_lower and has_digit and not contains_forbidden_chars):
                return True
            return False

        except Exception as e:
            raise PasswordFormatValidationException(f"An uncaught exception occurred: {e}")
