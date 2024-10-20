

class JSONStructurePrompt:
    def __init__(self) -> None:
        """
        Initializes the JSONStructurePrompt class.
        """
        pass

    @staticmethod
    def get_structure_prompt() -> str:
        """
        Returns the JSON structure prompt.

        Returns:
            str: The JSON structure prompt.
        """
        return """
            Ensure that your response is formatted as valid JSON, which will be parsed using `json.loads()` in Python. The JSON should have the following structure:
            <output>
            {
                "title": "<title>",
                "content": "<content>"
            }
            </output>
    
            YOU MUST include ONLY the JSON output without any additional text or commentary. Start your response with:
            <output>
            {
                "title":
                
            And end your response with:
            }
            </output>
        """
