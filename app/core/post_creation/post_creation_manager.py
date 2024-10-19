from app.config.logger_config import Logger
from app.excpetions.post_creation_exception.openai_completion_exception import OpenAICompletionException


class PostCreationManager:
    """A Class which manages the post creation process."""

    def __init__(self, request_id: str) -> None:
        """
        Initializes the class.

        Args:
            self

        Returns:
            None

        Raises:
            None
        """
        self.request_id: str = request_id

        self.created_posts: dict[str, dict[str, str]] = {}

        self.logger = Logger.get_logger()

    def start_post_creation(self) -> dict[str, dict[str:str]]:
        """
        Starts the post creation process and returns the created posts in a dictionary.

        Args:
            self

        Returns:
            dict[str, list[str]]: With the key as the service name and the value as dictionary with the created posts.

        Raises:
            None
        """
        self.logger.info(f"Handling post creation for request: {self.request_id}")

        try:
            NotImplemented
        except OpenAICompletionException as OCE:
            self.logger.error(f"While handling post creation for request: {self.request_id} the following error occurred: {OCE}")
