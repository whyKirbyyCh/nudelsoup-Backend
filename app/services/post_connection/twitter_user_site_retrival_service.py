

class TwitterUserSiteRetrivalService:
    """ A class for retrieving user site from Twitter. """

    @classmethod
    def get_user_site(cls, user_id: str) -> str:
        """
        Given a userId, returns the link of the user submissions.

        Args:
            user_id (str): The user id.

        Returns:
            str: The link of the user submissions.
        """
        return "https://x.com/mkbhd"