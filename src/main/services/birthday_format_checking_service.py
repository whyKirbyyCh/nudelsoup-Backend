from datetime import date

from src.main.dto.string_to_birthday_dto import StringToBirthday
from src.main.excpetions.account_signup_excpetions.birthday_format_validation_exception import BirthdayFormatValidationException


class BirthdayFormatChecker:
    """Class to check if a birthday has a valid format."""
    def __init__(self, birthday_string: str) -> None:
        """
        Initialize the BirthdayFormatChecker with the birthday to be checked.

        Args:
            birthday_string (str): The birthday to be checked.

        Returns:
            None

        Raises:
            TypeError: If the birthday is not a string.
            ValueError: If the birthday is empty.
        """
        if not birthday_string:
            raise ValueError("birthday must not be empty")

        if not isinstance(birthday_string, str):
            raise TypeError("birthday must be a string")

        self.birthday = StringToBirthday(birthday_string).to_date()

    def is_valid(self) -> bool:
        """
        Check if the birthday is valid.

        Args:

        Returns:
            bool: True if the birthday is valid, False otherwise.

        Raises:
            None
        """
        try:
            return self._is_valid_date()
        except BirthdayFormatValidationException:
            return False

    def _is_valid_date(self) -> bool:
        """
        Check if the birthday is a valid date. Meaning if the date is not in the future, or to far in the past.


        Args:

        Returns:
            bool: True if the birthday is a valid date, False otherwise.

        Raises:
            BirthdayFormatValidationException: If the birthday validation fails.
        """
        try:
            if self.birthday.year < 1930:
                return False
            if date(self.birthday.year, self.birthday.month, self.birthday.day) > date.today():
                return False

            return True

        except Exception as e:
            raise BirthdayFormatValidationException(f"Could not validate birthday format: {e}")

