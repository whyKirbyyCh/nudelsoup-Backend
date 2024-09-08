from validate_email_address import validate_email
import validators
from typing import Optional

from src.main.excpetions.account_signup_excpetions.email_format_validation_excpetion import EmailFormatValidationException
from src.main.excpetions.account_signup_excpetions.email_mxrecord_lookup_exception import EmailMXRecordLookupException
from src.main.excpetions.account_signup_excpetions.uncaught_email_format_checking_exception import UncaughtEmailFormatCheckingException


class EmailFormatChecker:
    """Class to check if an email has a valid format and domain."""
    def __init__(self, email: str, check_mx: Optional[bool] = False) -> None:
        """
        Initialize the EmailValidator with options for additional checks.

        Args:
            email (str): The email to be validated.
            check_mx (bool, optional): Whether to check for MX records. Defaults to False.

        Returns:
            None

        Raises:
            ValueError: If the email is not a string.
            TypeError: If the email is not a string or check_mx is not a boolean.
        """
        if not email:
            raise ValueError("email must not be empty")

        if not isinstance(email, str):
            raise TypeError("email must be a string")

        if not isinstance(check_mx, bool):
            raise TypeError("check_mx must be a boolean")

        self.email = email
        self.check_mx = check_mx

    def _is_valid_format(self) -> bool:
        """
        Check if the email has a valid format using the validator's library.

        Args:

        Returns:
            bool: True if the email has a valid format, False otherwise.

        Raises:
        """
        try:
            return validators.email(self.email)
        except Exception as e:
            raise EmailFormatValidationException(f"Could not validate email format: {e}")

    def _has_valid_domain(self) -> bool:
        """
        Check if the domain is valid, with an option to check MX records.

        Args:

        Returns:
            bool: True if the domain is valid, False otherwise.

        Raises:
            EmailMXRecordLookupException: If the domain is not valid and check_mx is True.
        """
        try:
            return validate_email(self.email, verify=self.check_mx)
        except Exception as e:
            raise EmailMXRecordLookupException(f"Could not validate email domain: {e}")

    def is_valid(self) -> bool:
        """
        Check if the email is valid in both format and domain.

        Args:

        Returns:
            bool: True if the email is valid, False otherwise.

        Raises:
             UncaughtEmailFormatCheckingException: If an exception is not caught.
        """
        try:
            return self._is_valid_format() and self._has_valid_domain()
        except EmailFormatValidationException as e:
            return False

        except EmailMXRecordLookupException as e:
            return False

        except Exception as e:
            raise UncaughtEmailFormatCheckingException(f"An uncaught exception occurred: {e}")
