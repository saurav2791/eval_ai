import requests
import logging
import json
import os
from typing import Union, Dict, List, Any
from pydantic import ValidationError
from evaluableai.exceptions import EvaluableAIError, NotFoundError, APIStatusError, PermissionDeniedError
from evaluableai.client import EvaluableAI

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

class Template:
    """
    Client for interacting with the Evaluable AI API.

    Attributes:
        id (str): ID of the template.
        name (str): Name of the template.
        prompt (str): Prompt of the template.
        context (str): Context of the template.
    """

    def __init__(self, id: str = None, name: str = None, prompt: str = None, context: str = None) -> None:
        """
        Initialize the Template with optional template details.

        Args:
            id (str): ID of the template.
            name (str): Name of the template.
            prompt (str): Prompt of the template.
            context (str): Context of the template.
        """
        self.client = EvaluableAI()
        self.id = id
        self.name = name
        self.prompt = prompt
        self.context = context

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle the response from the API.

        Args:
            response (requests.Response): The response object from the API request.

        Returns:
            dict: The response data.

        Raises:
            EvaluableAIError: If the response status code indicates an error.
        """
        if response.status_code in [200, 201]:
            logger.info("Successful response received.")
            return list(response.json()["data"].values())[0]
        elif response.status_code == 403:
            logger.error("403 - Access forbidden")
            raise PermissionDeniedError("403 - Access forbidden")
        elif response.status_code == 404:
            error_message = response.json().get("error")
            if error_message and "Template is already exists." in error_message:
                logger.error("Template with this name already exists.")
                raise NotFoundError("Template with this name already exists.", response=response, body=response.json())
            else:
                logger.error(f"Resource not found: {response.status_code} - {response.text}")
                raise NotFoundError(f"Resource not found: {response.status_code} - {response.text}", response=response, body=response.json())
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            raise EvaluableAIError(f"Error: {response.status_code} - {response.text}")

    def fetch(self, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]], str]:
        """
        Fetch the template(s) from the API.

        Returns:
            dict or list: The fetched template data.

        Raises:
            NotFoundError: If the template is not found.
            EvaluableAIError: For other API errors.
        """
        id_to_fetch = kwargs.get("id", self.id) if kwargs else self.id
        try:
            endpoint = config['template_fetch'].replace("{template_id}", id_to_fetch) if id_to_fetch else config['template_fetch_all']
            logger.info(f"Fetching template with ID: {id_to_fetch}")
            response = self.client.make_request("GET", endpoint)
            return self._handle_response(response)
        except requests.RequestException as e:
            logger.error(f"FETCH request failed: {str(e)}")
            raise EvaluableAIError(f"FETCH request failed: {str(e)}")
        except NotFoundError as e:
            raise e

    def create(self) -> Union[str, None]:
        """
        Create a new template in the API.

        Returns:
            str: The ID of the created template.

        Raises:
            ValidationError: If the input data is invalid.
            EvaluableAIError: For other API errors.
        """
        if self.name is None or self.prompt is None:
            logger.error("Error: Missing required arguments 'name' and 'prompt'")
            return None

        endpoint = config['template_create']
        try:
            data = {
                "name": self.name,
                "prompt": self.prompt,
                "context": self.context
            }
            logger.info(f"Creating template with name: {self.name}")
            response = self.client.make_request("POST", endpoint, data)
            result = self._handle_response(response)
            self.id = result.get("id")
            self.name = result.get("name")
            self.prompt = result.get("prompt")
            self.context = result.get("context")
            return self.id
        except (ValidationError, ValueError) as error:
            logger.error(f"Validation or Value error: {error}")
            raise error
        except requests.RequestException as e:
            logger.error(f"CREATE request failed: {str(e)}")
            raise EvaluableAIError(f"CREATE request failed: {str(e)}")

    def remove(self, **kwargs) -> str:
        """
        Remove a template from the API.

        Returns:
            str: A message confirming the deletion.

        Raises:
            NotFoundError: If the template is not found.
            EvaluableAIError: For other API errors.
        """
        id_to_delete = kwargs.get("id", self.id) if kwargs else self.id
        if not id_to_delete:
            raise ValueError("Template ID is required for deletion.")
        try:
            endpoint = config['template_delete'].replace("{template_id}", id_to_delete)
            logger.info(f"Removing template with ID: {id_to_delete}")
            response = self.client.make_request("DELETE", endpoint)
            message = response.json()["message"]
            self.id = None
            return f"Template data {id_to_delete} deleted. {message}"
        except requests.RequestException as e:
            logger.error(f"REMOVE request failed: {str(e)}")
            raise EvaluableAIError(f"REMOVE request failed: {str(e)}")
        except NotFoundError as e:
            raise e

    def update(self, **kwargs) -> Union[Dict[str, Any], ValidationError]:
        """
        Update a template in the API.

        Returns:
            dict: The updated template data.

        Raises:
            ValidationError: If the input data is invalid.
            EvaluableAIError: For other API errors.
        """
        try:
            if self.id:
                current_template = self.fetch()
                if not current_template:
                    raise NotFoundError(f"Template with id {self.id} not found")

                self.name = kwargs.get("name", self.name if self.name else current_template.get("name"))
                self.prompt = kwargs.get("prompt", self.prompt if self.prompt else current_template.get("prompt"))
                self.context = kwargs.get("context", self.context if self.context else current_template.get("context"))

            data = {
                "id": self.id,
                "name": self.name,
                "prompt": self.prompt,
                "context": self.context
            }

            for key, value in kwargs.items():
                if value is not None:
                    data[key] = value
            logger.info(f"Updating template with ID: {self.id}")
            endpoint = config['template_update'].replace("{template_id}", self.id)
            response = self.client.make_request("PUT", endpoint, data)
            if response.status_code == 400 and "Template is already exists." in response.text:
                raise ValueError("Template with this name already exists.")
            updated_template = self._handle_response(response)

            self.id = updated_template.get("id")
            self.name = updated_template.get("name")
            self.prompt = updated_template.get("prompt")
            self.context = updated_template.get("context")

            return updated_template
        except ValidationError as error:
            logger.error(f"Validation error: {error}")
            return error
        except requests.RequestException as e:
            logger.error(f"UPDATE request failed: {str(e)}")
            raise EvaluableAIError(f"UPDATE request failed: {str(e)}")

    def restore(self) -> Union[Dict[str, Any], List[Dict[str, Any]], ValidationError]:
        """
        Restore a deleted template in the API.

        Returns:
            dict or list: The restored template data.

        Raises:
            ValidationError: If the input data is invalid.
            EvaluableAIError: For other API errors.
        """
        endpoint = config['template_restore'].replace("{template_id}", self.id) if self.id else config['template_restore_all']
        try:
            logger.info(f"Restoring template with ID: {self.id}")
            response = self.client.make_request("PUT", endpoint)
            return self._handle_response(response)
        except ValidationError as error:
            logger.error(f"Validation error: {error}")
            return error
        except requests.RequestException as e:
            logger.error(f"RESTORE request failed: {str(e)}")
            raise EvaluableAIError(str(e))

    def list_of_deletion(self) -> List[Dict[str, Any]]:
        """
        List all deleted templates.

        Returns:
            list: A list of deleted templates.

        Raises:
            EvaluableAIError: For API errors.
        """
        try:
            logger.info("Listing all deleted templates")
            endpoint = config['template_list_deletions']
            response = self.client.make_request("GET", endpoint)
            deleted_templates = self._handle_response(response)
            return deleted_templates if deleted_templates else "None of the template objects deleted."
        except requests.RequestException as e:
            logger.error(f"LIST OF DELETION request failed: {str(e)}")
            raise EvaluableAIError(str(e))

    def get_all_templates(self) -> Union[Dict[str, Any], APIStatusError]:
        """
        Get all templates of a user.

        Returns:
            dict: The fetched templates data.

        Raises:
            PermissionDeniedError: If the user does not have permission to view the resource.
            APIStatusError: For other API errors.
        """
        try:
            logger.info("Fetching all templates")
            endpoint = config['template_get_all']
            response = self.client.make_request("GET", endpoint)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                raise PermissionDeniedError("User does not have permission to perform this operation")
            else:
                raise APIStatusError(f"Unexpected error: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            logger.error(f"GET ALL TEMPLATES request failed: {str(e)}")
            raise APIStatusError(f"GET request failed: {str(e)}")

    def create_templates_in_bulk(self, templates: List[Dict[str, Any]]) -> Union[Dict[str, Any], APIStatusError]:
        """
        Create bulk templates via JSON array.

        Args:
            templates (list): List of template dictionaries.

        Returns:
            dict: The job ID and status of the batch job.

        Raises:
            PermissionDeniedError: If the user does not have permission to create the resource.
            APIStatusError: For other API errors.
        """
        try:
            logger.info("Creating templates in bulk")
            endpoint = config['template_bulk_create']
            response = self.client.make_request("POST", endpoint, data={"templates": templates})
            if response.status_code == 201:
                return response.json()
            elif response.status_code == 403:
                raise PermissionDeniedError("User does not have permission to perform this operation")
            else:
                raise APIStatusError(f"Unexpected error: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            logger.error(f"CREATE TEMPLATES IN BULK request failed: {str(e)}")
            raise APIStatusError(f"POST request failed: {str(e)}")

    def bulk_delete(self, template_ids: List[str]) -> Union[Dict[str, Any], APIStatusError]:
        """
        Bulk delete templates by their IDs.

        Args:
            template_ids (list): List of template IDs to be deleted.

        Returns:
            dict: The status of the bulk delete operation.

        Raises:
            PermissionDeniedError: If the user does not have permission to delete the resource.
            APIStatusError: For other API errors.
        """
        try:
            logger.info(f"Bulk deleting templates with IDs: {template_ids}")
            endpoint = config['template_bulk_delete']
            response = self.client.make_request("POST", endpoint, data={"template_ids": template_ids})
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                raise PermissionDeniedError("User does not have permission to perform this operation")
            else:
                raise APIStatusError(f"Unexpected error: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            logger.error(f"BULK DELETE request failed: {str(e)}")
            raise APIStatusError(f"POST request failed: {str(e)}")
