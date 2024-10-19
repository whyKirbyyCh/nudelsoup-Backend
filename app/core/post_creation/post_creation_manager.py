from app.config.logger_config import Logger
from app.excpetions.post_creation_exception.openai_completion_exception import OpenAICompletionException
from app.excpetions.post_creation_exception.posts_creation_exception import PostsCreationException
from typing import Tuple, Dict
import traceback


class PostCreationManager:
    """A Class which manages the post creation process."""

    def __init__(self, request_id: str, order: Dict[str, Dict[str, str]]) -> None:
        """
        Initializes the PostCreationManager instance.

        Args:
            request_id (str): The unique identifier for the request.
            order (Dict[str, Dict[str, str]]): The order details.
        """
        self.request_id: str = request_id
        self.order: Dict[str, Dict[str, str]] = order

        self.created_posts: Dict[str, Dict[str, str]] = {}

        self.logger = Logger.get_logger()

    def _start_post_creation(self) -> Dict[str, Dict[str, str]]:
        """
        Starts the post creation process and returns the created posts in a Dictionary.

        Returns:
            Dict[str, list[str]]: With the key as the service name and the value as Dictionary with the created posts.

        Raises:
            PostsCreationException: If an error occurs while creating the posts.
        """
        self.logger.info(f"Handling post creation for request: {self.request_id}")

        try:
            post_setups: Dict[str, Tuple[str, str]] = self._get_post_setups()

        except OpenAICompletionException as OCE:
            self.logger.error(f"Error with OpenAI API: {OCE}")
            raise PostsCreationException(f"OpenAI API error: {OCE}") from OCE

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
            raise PostsCreationException("An unexpected error occurred.") from e

    def _get_post_setups(self) -> Dict[str, Tuple[str, str]]:
        """
        Returns the post setups for each service.

        Returns:
            Dict[str, Tuple[str, str]]: The post setups for each service, which includes a system prompt and a user prompt.

        Raises:
            PostsCreationException: If an error occurs while collecting the post setups.
        """
        try:
            company_info = self.order["company_info"]
            for service_name, service_details in self.order.items():
                self.logger.info(f"Collecting post setups for service: {service_name}, order: {service_details}")

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
            raise PostsCreationException("An unexpected error occurred.") from e

    def get_posts(self) -> Dict[str, Dict[str, str]]:
        """
        Returns the created posts.

        Returns:
            Dict[str, Dict[str, str]]: The created posts.

        Raises:
            PostsCreationException: If an error occurs while getting the created posts.
        """
        return self._start_post_creation()


if __name__ == "__main__":
    post_creation_manager = PostCreationManager(request_id="123", order={"reddit": {"type": "text", "user_prompt": "What is the meaning of life?", "system_prompt": "You are a helpful assistant."}, "twitter": {"type": "text", "user_prompt": "What is the meaning of life?", "system_prompt": "You are a helpful assistant."}})
    results = post_creation_manager.get_posts()
