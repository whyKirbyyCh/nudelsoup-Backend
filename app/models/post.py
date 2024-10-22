from typing import Dict


class Post:
    """Class representing a post."""

    def __init__(self, user_id: str, product_id: str, campaign_id: str, site: str, title: str, content: str, created_at: str) -> None:
        """
        Initializes the class with the id, title, content, and created_at.

        Args:
            user_id (str): The id of the user.
            product_id (str): The id of the product.
            campaign_id (str): The id of the campaign.
            site (str): The site of the post.
            title (str): The title of the post.
            content (str): The content of the post.
            created_at (str): The date and time when the post was created.

        """
        self.user_id: str = user_id
        self.product_id: str = product_id
        self.campaign_id: str = campaign_id
        self.site: str = site
        self.title: str = title
        self.content: str = content
        self.created_at: str = created_at

    def to_dict(self) -> Dict[str, str]:
        """
        Converts the object to a dictionary.

        Returns:
            Dict[str, str]: The dictionary representation of the object.
        """
        return {
            "userId": self.user_id,
            "productId": self.product_id,
            "campaignId": self.campaign_id,
            "site": self.site,
            "title": self.title,
            "content": self.content,
            "createdAt": self.created_at,
            "updatedAt": self.created_at
        }
