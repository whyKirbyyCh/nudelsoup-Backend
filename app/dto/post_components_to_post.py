from app.models.post import Post
from typing import List, Dict
import time


class PostComponentsToPost:

    @classmethod
    def convert_to_posts(cls, posts: Dict[str, Dict[str, str]], user_id: str, product_id: str, campaign_id: str) -> List[Post]:
        """
        Converts the post components to Post objects.

        Args:
            posts (Dict[str, Dict[str, str]]): The dictionary of post components where the key is the site.
            user_id (str): The ID of the user.
            product_id (str): The ID of the product.
            campaign_id (str): The ID of the campaign.

        Returns:
            List[Post]: The converted list of Post objects.
        """
        return [
            Post(
                user_id=user_id,
                product_id=product_id,
                campaign_id=campaign_id,
                site=site,
                title=post_data["title"],
                content=post_data["content"],
                created_at=time.strftime("%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)", time.gmtime())
            )
            for site, post_data in posts.items()
        ]
