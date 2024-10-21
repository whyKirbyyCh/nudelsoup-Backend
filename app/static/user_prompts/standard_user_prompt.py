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
        additional_info: str = "\n".join(
            f"{key[11:]}: {value}" for key, value in self.product_info.items() if key.startswith("additional_")
        )

        prompt: str = f"""
        We would like to create a social media post about our product: {self.product_info.get("product_name", "N/A")}. When would describe it like this: {self.product_info.get("product_description", "N/A")}.
        
        The product business model is: {self.product_info.get("product_business_model", "N/A")}. And we see the product as a: {self.product_info.get("product_type", "N/A")}. 
        We think the best market for this product is {self.product_info.get("product_market", "N/A")}, and we would like to target this market on the site. """

        if additional_info:
            prompt += f"\nWe just wanted to mention the following details about our product:\n{additional_info}\n"

        prompt += """
        You can incorporate the things as you see fit for the information given.
        
        Please make the post honest, not marketing like, meaning not too over the top. Please make the post clear and concise and try to make it fit the market on the site as best as possible.
        """

        return prompt
