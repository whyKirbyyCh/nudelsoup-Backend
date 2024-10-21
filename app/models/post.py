

class Post:
    """Class representing a post."""

    def __init__(self, post_id: str, user_id: str, product_id: str, campaign_id: str, title: str, content: str, created_at: str) -> None:
        """
        Initializes the class with the id, title, content, and created_at.

        Args:
            post_id (str): The id of the post.
            title (str): The title of the post.
            content (str): The content of the post.
            created_at (str): The date and time when the post was created.

        Returns:
            None

        Raises:
            None
        """
        self.post_id: str = post_id
        self.user_id: str = user_id
        self.product_id: str = product_id
        self.campaign_id: str = campaign_id
        self.title: str = title
        self.content: str = content
        self.created_at: str = created_at
