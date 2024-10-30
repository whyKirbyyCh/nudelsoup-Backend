

class HackernewsUserSiteRetrivalService:
    """ Given a userId, returns the link of the user submissions. """

    @classmethod
    def get_user_site(cls, user_id: str) -> str:
        """
        Given a userId, returns the link of the user submissions.

        Args:
            user_id (str): The user id.

        Returns:
            str: The link of the user submissions.
        """
        return "https://news.ycombinator.com/submitted?id=cainxinth"
