import json
from json_repair import repair_json
import re


class JSONParsingService:
    """A class for parsing JSON data."""

    def __init__(self) -> None:
        """
        Initializes the JSONParsingService class.
        """
        pass

    @staticmethod
    def get_title_and_content(input_data: str) -> tuple:
        """
        Extracts the JSON data between <output> and </output>,
        repairs and parses it, then extracts 'title' and 'content'.

        Returns:
            tuple: A tuple containing the title and content.

        Raises:
            ValueError: If the JSON data is invalid even after repair.
        """
        pattern: str = r"<output>(.*?)</output>"
        match: re.Match = re.search(pattern, input_data, re.DOTALL)
        if match:
            json_content = match.group(1).strip()
        else:
            raise ValueError("No JSON content found between <output> and </output>")

        repaired_json: str = repair_json(json_content)

        try:
            parsed_data = json.loads(repaired_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data even after repair: {e}")

        return parsed_data.get("title", ""), parsed_data.get("content", "")
