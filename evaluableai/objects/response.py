import json
import logging
import os
import httpx
from dataclasses import dataclass, field
from typing import Set, Optional, Dict, Any
from evaluableai.client import EvaluableAI
from evaluableai.exceptions import (
    EvaluableAIError,
    PermissionDeniedError,
    NotFoundError,
    BadRequestError,
    APIStatusError
)
from evaluableai.objects.tag import Tag
from evaluableai.objects.candidate_model import CandidateModel
from evaluableai.objects.input import Input

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to load the endpoint configuration from the endpoint.json file
def load_config() -> dict:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(current_dir, '..', 'endpoint.json')
    config_file = os.path.normpath(config_file)

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found at: {config_file}")

    with open(config_file, 'r') as f:
        return json.load(f)

# Load the configuration once for global usage
config = load_config()

@dataclass
class Response:
    response_id: str
    text: str
    input: Input
    tags: Set[Tag] = field(default_factory=set)
    candidate_model: Optional[CandidateModel] = None
    choices_json_data: Optional[Dict[str, Any]] = None
    meta_data: Optional[str] = None

    @staticmethod
    def handle_response(response: httpx.Response) -> Dict[str, Any]:
        """
        Handle the HTTP response and raise exceptions for any errors.

        Args:
            response (httpx.Response): The response object.

        Returns:
            dict: The parsed JSON response.

        Raises:
            BadRequestError: For HTTP 400 errors.
            PermissionDeniedError: For HTTP 403 errors.
            NotFoundError: For HTTP 404 errors.
            APIStatusError: For other HTTP errors.
        """
        logger.info(f"Handling response with status code: {response.status_code}")
        if response.status_code in {200, 201}:
            return response.json()
        elif response.status_code == 400:
            logger.error("Bad Request: 400")
            raise BadRequestError(message="Bad Request", response=response, body=response.json())
        elif response.status_code == 403:
            logger.error("Forbidden: 403")
            raise PermissionDeniedError(message="Forbidden", response=response, body=response.json())
        elif response.status_code == 404:
            logger.error(f"Resource not found: 404 at {response.request.url}")
            raise NotFoundError(message=f"Resource not found at {response.request.url}", response=response,
                                body=response.json())
        else:
            logger.error(f"Unexpected status code: {response.status_code}")
            raise APIStatusError(message=f"Unexpected status code {response.status_code}", response=response,
                                 body=response.json())

    @classmethod
    def create_response(cls, client: EvaluableAI, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a response by sending a POST request to the specified endpoint.

        Args:
            client (EvaluableAI): The client instance.
            data (dict): The data payload.

        Returns:
            dict: The created response data.

        Raises:
            EvaluableAIError: If the request fails.
        """
        endpoint = config['response_create']  # Load from config
        logger.info(f"Creating response at endpoint: {endpoint}")
        try:
            response = client.make_request(method="POST", endpoint=endpoint, data=data)
            return cls.handle_response(response)
        except Exception as e:
            logger.error(f"Error creating response at {endpoint}: {str(e)}")
            raise EvaluableAIError(f"Error creating response for {endpoint}: {str(e)}")

    @classmethod
    def get_response_by_id(cls, client: EvaluableAI, response_id: str) -> Dict[str, Any]:
        """
        Get a response by its ID.

        Args:
            client (EvaluableAI): The client instance.
            response_id (str): The ID of the response to retrieve.

        Returns:
            dict: The fetched response data.

        Raises:
            EvaluableAIError: If the request fails.
        """
        endpoint = config['response_get_by_id'].replace("{response_id}", response_id)  # Load from config
        logger.info(f"Fetching response with ID: {response_id}")
        response = client.make_request(method="GET", endpoint=endpoint)
        return cls.handle_response(response)

    @classmethod
    def delete_response_by_id(cls, client: EvaluableAI, response_id: str) -> Dict[str, Any]:
        """
        Delete a response by its ID.

        Args:
            client (EvaluableAI): The client instance.
            response_id (str): The ID of the response to delete.

        Returns:
            dict: The deletion status.

        Raises:
            EvaluableAIError: If the request fails.
        """
        endpoint = config['response_delete_by_id'].replace("{response_id}", response_id)  # Load from config
        logger.info(f"Deleting response with ID: {response_id}")
        response = client.make_request(method="DELETE", endpoint=endpoint)
        return cls.handle_response(response)
