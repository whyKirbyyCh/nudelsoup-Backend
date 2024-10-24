import os
from openai import OpenAI
from app.config.logger_config import Logger
from dataclasses import dataclass
from dotenv import load_dotenv
from app.excpetions.post_creation_exception.openai_completion_exception import OpenAICompletionException
from typing import Optional


@dataclass
class OpenAIConnection:
    """Handles the connection to the OpenAI API."""
    model: str = "gpt-4o-mini"

    def __post_init__(self) -> None:
        """
        Initializes the OpenAI API key and logger.

        Args:
            self

        Returns:
            None

        Raises:
            ValueError: If the OpenAI API key is not set in the environment variables.

        """
        load_dotenv(override=True)

        self.api_key: str = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("OpenAI API key is not set in the environment variables.")

        self.logger = Logger.get_logger()

        self.client: OpenAI = OpenAI(api_key=self.api_key)

    def create_post(self, user_prompt: str, system_prompt: str, max_tokens: Optional[int] = None) -> str:
        """
        Generates a post using the OpenAI API.

        Args:
            user_prompt (str): The user-provided prompt.
            system_prompt (str): The system prompt for the assistant.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to None.

        Returns:
            str: The generated response from the OpenAI API.

        Raises:
            RuntimeError: If an error occurs while generating the post.
        """
        try:
            if max_tokens is None:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    max_tokens=max_tokens
                )
            return response.choices[0].message.content
        except Exception as ex:
            raise OpenAICompletionException(f"An error occurred while generating the post: {ex}")


if __name__ == "__main__":
    try:
        openai_connection = OpenAIConnection(model="gpt-4o-mini")
        result = openai_connection.create_post(
            user_prompt="What is the meaning of life?",
            system_prompt="You are a helpful assistant."
        )
        print(result)
    except Exception as e:
        print(f"Error: {e}")
