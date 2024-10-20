from typing import Dict


class StandardUserPrompt:
    def __init__(self, product_info: Dict[str, str]) -> None:
        """
        Initializes the class with the user prompt.
        """
        raise NotImplementedError

    def get_user_prompt(self) -> str:
        """
        Returns the user prompt for the standard user.

        Returns:
            str: The user prompt for the standard user.
        """
        raise NotImplementedError