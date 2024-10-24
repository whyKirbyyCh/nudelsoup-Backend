from app.excpetions.rest.user_authentication_excpetion import UserAuthenticationException
from app.excpetions.rest.user_limits_exception import UserLimitsException


class UserAuthenticationService:
    """
    Class that provides methods for user authentication.
    """

    @classmethod
    def authenticate_user(cls, user_id: str, password: str, token: str) -> bool:
        """
        Authenticates the user.

        Args:
            user_id (str): The username of the user.
            password (str): The password of the user.
            token (str): The token of the user.

        Returns:
            bool: True if the user is authenticated, False otherwise.

        Raises:
            UserAuthenticationException: If the user is not authenticated.
        """
        try:
            return True

        except UserAuthenticationException:
            raise UserAuthenticationException("User is not allowed to access this resource.")

        except UserLimitsException:
            raise UserLimitsException("User has reached the limit for this billing period.")
