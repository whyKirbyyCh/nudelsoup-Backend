from typing import Dict


class StandardUserPrompt:
    def __init__(self, product_info: Dict[str, str]) -> None:
        """
        Initializes the class with the user prompt.

        Args:
            product_info (Dict[str, str]): The product information to be used in the prompt.

        Raises:
            ValueError: If the product info is empty.
        """
        if not product_info:
            raise ValueError("product_info must not be empty")

        self.product_info: Dict[str, str] = product_info

    def get_user_prompt(self) -> str:
        """
        Returns the user prompt for the standard user.

        Returns:
            str: The user prompt for the standard user.
        """
        return """Please create a post with a title and content for the mentioned company for the launch of their new product which does autimatic social media marketing for small companies. """