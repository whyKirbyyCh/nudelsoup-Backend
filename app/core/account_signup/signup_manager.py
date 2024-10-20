from typing import Optional, Any

from app.services.email_format_checking_service import EmailFormatChecker
from app.services.password_format_checking_service import PasswordFormatChecker
from app.services.birthday_format_checking_service import BirthdayFormatChecker
from app.core.account_signup.producthunt_signup import ProducthuntSignup


class SignupManager:
    """Class that is used to manage the account creation process for the selected services."""

    def __init__(self, services: list[str], username: str, email: str, password: str, name: str, surname: str, birthdate: str, gmail_credentials: Optional[dict[str, str]] = None) -> None:
        """
        Initializes the class with the selected services, username, email, password, name, surname, month, day, and year.

        Args:
            services (list[str]): The list of services for which an account needs to be created.
            username (str): The username to be used in the account creation process.
            email (str): The email to be used in the account creation process.
            password (str): The password to be used in the account creation process.
            name (str): The name to be used in the account creation process.
            surname (str): The surname to be used in the account creation process.
            birthdate (str): The birthdate to be used in the account creation process.
        """
        self.services: list[str] = services
        self.username: str = username
        self.email: str = email
        self.password: str = password
        self.name: str = name
        self.surname: str = surname
        self.birthdate: str = birthdate
        self.gmail_credentials: Optional[dict[str, str]] = gmail_credentials

        self.serviceObjects: dict[str, Any] = {}
        self.serviceCredentials: dict[str, dict[str, str]] = {}
        self.notExistingServices: list[str] = []

    def create_account(self) -> bool:
        """
        Creates an account for the selected services.

        Args:

        Returns:
            bool: True if the account was created successfully, False otherwise.

        Raises:
            None
        """
        if not self._validate_credentials():
            return False

        for service in self.services:
            if service == "producthunt":
                self.serviceObjects["producthunt"] = ProducthuntSignup(self.username, self.email, self.password, self.name, self.surname)
                self.serviceCredentials["producthunt"] = {"username": self.gmail_credentials["username"], "password": self.gmail_credentials["password"], "email": self.email}
                self.serviceObjects["producthunt"].create_account()
            else:
                self.notExistingServices.append(service)

    def _validate_credentials(self) -> bool:
        """
        Validates the credentials of the account creation process.

        Args:

        Returns:
            None

        Raises:
            None
        """
        self.email_format_checker: EmailFormatChecker = EmailFormatChecker(self.email, check_mx=True)
        self.password_format_checker: PasswordFormatChecker = PasswordFormatChecker(self.password)
        self.birthday_format_checker: BirthdayFormatChecker = BirthdayFormatChecker(self.birthdate)

        if not (self.email_format_checker.is_valid() and self.password_format_checker.is_valid() and self.birthday_format_checker.is_valid()):
            return False

        return True
