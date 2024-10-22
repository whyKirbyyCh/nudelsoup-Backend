from app.config.logger_config import Logger
from app.excpetions.post_creation_exception.openai_completion_exception import OpenAICompletionException
from app.excpetions.post_creation_exception.posts_creation_exception import PostsCreationException
from app.static.system_prompts.standard_system_prompt import StandardSystemPrompt
from app.static.user_prompts.standard_user_prompt import StandardUserPrompt
from app.static.user_prompts.json_structure_prompt import JSONStructurePrompt
from app.core.post_creation.openai_connection import OpenAIConnection
from app.models.order import Order
from app.services.post_creation.json_parsing_service import JSONParsingService
from typing import Tuple, Dict, List
import traceback
from app.services.post_creation.post_archive_service import PostArchiveService
from app.dto.post_components_to_post import PostComponentsToPost
from app.models.post import Post


class PostCreationManager:
    """A Class which manages the post creation process."""

    def __init__(self, request_id: str, order: Order, user_id: str, campaign_id: str, product_id: str) -> None:
        """
        Initializes the PostCreationManager instance.

        Args:
            request_id (str): The unique identifier for the request.
            order (Dict[str, Dict[str, str]]): The order details.
            user_id (str): The unique identifier for the user.
            campaign_id (str): The unique identifier for the campaign.
            product_id (str): The unique identifier for the product.
        """
        self.request_id: str = request_id
        self.order: Dict[str, Dict[str, Dict[str, str]]] = order.order_details
        self.services: Dict[str, bool] = order.services
        self.company_info: Dict[str, Dict[str, str]] = order.company_info
        self.product_info: Dict[str, Dict[str, str]] = order.product_info
        self.user_id: str = user_id
        self.campaign_id: str = campaign_id
        self.product_id: str = product_id

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

        created_posts: Dict[str, Dict[str, str]] = {}

        json_parsing_service: JSONParsingService = JSONParsingService()

        standard_system_prompt: str = StandardSystemPrompt(self.company_info).get_system_prompt()
        standard_user_prompt: str = StandardUserPrompt(self.product_info).get_user_prompt()
        json_structure_prompt: str = JSONStructurePrompt().get_structure_prompt()

        try:
            post_setups: Tuple[Dict[str, Tuple[str, str]], Dict[str, Tuple[str, str]]] = self._create_post_setups()

            for service, is_enabled in self.services.items():
                if is_enabled:
                    system_prompt: str = standard_system_prompt + post_setups[0][service][0] + post_setups[0][service][1]
                    user_prompt: str = standard_user_prompt + post_setups[1][service][0] + post_setups[1][service][1] + json_structure_prompt

                    response: str = OpenAIConnection().create_post(user_prompt=user_prompt, system_prompt=system_prompt)

                    response: Tuple[str, str] = json_parsing_service.get_title_and_content(response)
                    created_posts[service] = {"title": response[0], "content": response[1]}

            posts: List[Post] = PostComponentsToPost().convert_to_posts(posts=created_posts, user_id=self.user_id, campaign_id=self.campaign_id, product_id=self.product_id)

            PostArchiveService().archive_posts(posts=posts)

            return created_posts

        except OpenAICompletionException as OCE:
            self.logger.error(f"Error with OpenAI API: {OCE}")
            raise PostsCreationException(f"OpenAI API error: {OCE}") from OCE

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
            raise PostsCreationException("An unexpected error occurred.") from e

    def _create_post_setups(self) -> Tuple[Dict[str, Tuple[str, str]], Dict[str, Tuple[str, str]]]:
        """
        Returns the post setups for each service.

        Returns:
            Dict[str, Tuple[str, str]]: The post setups for each service, which includes a system prompt and a user prompt.

        Raises:
            PostsCreationException: If an error occurs while collecting the post setups.
        """
        try:
            combined_system_prompt: Dict[str, Tuple[str, str, str]] = self._combine_prompt_dict(
                dict1=self.order["system"]["sscop"],
                dict2=self.order["system"]["cpop"]
            )
            combined_user_prompt: Dict[str, Tuple[str, str, str]] = self._combine_prompt_dict(
                dict1=self.order["user"]["sspop"],
                dict2=self.order["user"]["ppsop"]
            )

            return combined_system_prompt, combined_user_prompt

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
            raise PostsCreationException("An unexpected error occurred in the prompt setup process.") from e

    def _combine_prompt_dict(self, dict1: Dict[str, str], dict2: Dict[str, str]) -> Dict[str, Tuple[str, str]]:
        """
        Combines two prompt dictionaries.

        Args:
            dict1 (Dict[str, str]): The first dictionary.
            dict2 (Dict[str, str]): The second dictionary.

        Returns:
            Dict[str, Tuple[str, str]]: The combined dictionary.
        """

        combined: Dict[str, Tuple[str, str]]

        if "all" in dict1 and "all" in dict2:
            combined = {key: (dict1["all"][0], dict2["all"][0]) for key, value in self.services.items() if value}
        elif "all" in dict1:
            combined = {key: (dict1["all"][0], dict2[key]) for key in dict2}
        elif "all" in dict2:
            combined = {key: (dict1[key], dict2["all"][0]) for key in dict1}
        else:
            combined = {key: (dict1[key], dict2[key]) for key in dict1.keys() & dict2.keys()}

        return combined

    def get_posts(self) -> Dict[str, Dict[str, str]]:
        """
        Returns the created posts.

        Returns:
            Dict[str, Dict[str, str]]: The created posts.

        Raises:
            PostsCreationException: If an error occurs while getting the created posts.
        """
        return self._start_post_creation()
