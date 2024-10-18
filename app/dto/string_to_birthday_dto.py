from dateutil import parser
from datetime import datetime, date

from src.main.models.birthday import Birthday
from src.main.excpetions.account_signup_excpetions.birthday_parsing_exception import BirthdayParsingException


class StringToBirthday:
    """Class that is used to convert a string to a Birthday object."""

    def __init__(self, date_string: str):
        """
        Initializes the class with the string to be converted.

        Args:
            date_string (str): The string to be converted.

        Raises:
            TypeError: If the input is not a string.
            ValueError: If the string is empty.
        """
        if not isinstance(date_string, str):
            raise TypeError("date_string must be a string")
        if not date_string.strip():
            raise ValueError("date_string must not be empty")

        self.date_string = date_string.strip()

    def to_date(self, formats: list[str] = None) -> Birthday:
        """
        Convert the string to a Birthday object.

        Args:
            formats (list[str], optional): List of format strings to try.
                                           If None, uses flexible parsing.

        Returns:
            Birthday: The Birthday object.

        Raises:
            None
        """
        return self._parse_flexible()

    def _parse_flexible(self) -> Birthday:
        """
        Attempt to parse the date string using flexible parsing.

        Args:

        Returns:
            Birthday: The Birthday object.

        Raises:
            BirthdayParsingException: If the string cannot be parsed into a valid date.
        """
        try:
            parsed_date: date = parser.parse(self.date_string, fuzzy=True).date()
            return Birthday(parsed_date.year, parsed_date.month, parsed_date.day)
        except (ValueError, OverflowError):
            raise BirthdayParsingException(f"Unable to parse '{self.date_string}' into a valid date")
