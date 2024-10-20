from typing import Dict


class StandardSystemPrompt:
    """Class that represents the standard user prompt, used when no other prompt is specified."""

    def __init__(self, company_info: Dict[str, str]) -> None:
        """
        Initializes the StandardUserPrompt class.

        Args:
            company_info (Dict[str, str]): The company information to be used in the prompt.
        """
        self.company_info: Dict[str, str] = company_info

    def get_system_prompt(self) -> str:
        """
        Returns the user prompt for the standard user.

        Returns:
            str: The user prompt for the standard user.
        """
        additional_info: str = "\n".join(
            f"{key[11:]}: {value}" for key, value in self.company_info.items() if key.startswith("additional_")
        )

        prompt = f"""
        You are a marketing assistant for a company, which does automatic social media marketing for small companies.\n
        Our service is the following:\n
        A customer can select a social media services such as Facebook, Instagram, Twitter, LinkedIn, Reddit and many more, from a list and ask us to create the post for them. Tailored to their needs and company, to help them grow their business.\n
        They will tell you about the platform, what they hope to achieve from the post on the platform and any special remarks they have.\n\n
        
        Right now your are working on the case of a company called {self.company_info.get("company_name", "N/A")}.\n
        They are based in {self.company_info.get("company_country", "N/A")} and have {self.company_info.get("company_size", "N/A")} employees.\n 
        The company has been in business for {self.company_info.get("company_age", "N/A")} years and operates in the {self.company_info.get("company_industry", "N/A")} industry.\n\n
        The company describes itself as {self.company_info.get("company_description", "N/A")}.\n
        """

        if additional_info:
            prompt += f"\nThey would like you to know the following details about them:\n{additional_info}\n"

        prompt += """
        Your task is to assist the company in growing its business by supporting their social media initiatives. 
        Follow their instructions carefully, ensuring that your responses are clear and concise. 
        Your role is to execute their requests precisely without adding, changing, or critiquing their instructions. 
        Assume that all directives have been thoroughly considered and finalized.
        """

        return prompt.strip()
