import logging
import os
import json
from evaluableai.client import EvaluableAI
from evaluableai.exceptions import EvaluableAIError, NotFoundError, APIStatusError, PermissionDeniedError

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

class Tag:
    def __init__(self, client: EvaluableAI):
        self.client = client

    def create_tag(self, tag_name, color=None):
        if not tag_name:
            raise ValueError("Tag name is required")

        data = {
            "tag_name": tag_name,
            "color": color,
        }
        endpoint = config['tag_create']
        response = self.client.make_request(method="POST", endpoint=endpoint, data=data)
        self._handle_response(response)
        return response.json()

    def create_tags_bulk(self, tags):
        for tag in tags:
            if 'tag_name' not in tag:
                raise ValueError("Tag name is required for all tags")

        data = tags
        logger.info(f"Creating bulk tags with data: {data}")
        endpoint = config['tag_create_bulk']
        response = self.client.make_request(method="POST", endpoint=endpoint, data=data)
        self._handle_response(response)
        return response.json()

    def update_tag(self, tag_id, tag_name=None, color=None):
        data = {}
        if tag_name:
            data['tag_name'] = tag_name
        if color:
            data['color'] = color
        logger.info(f"Updating tag {tag_id} with data: {data}")
        endpoint = config['tag_update'].replace("{tag_id}", tag_id)
        response = self.client.make_request(method="PUT", endpoint=endpoint, data=data)
        self._handle_response(response)
        return response.json()

    def get_tag_by_name(self, tag_name):
        logger.info(f"Fetching tag by name: {tag_name}")
        endpoint = config['tag_get_by_name'].replace("{tag_name}", tag_name)
        response = self.client.make_request(method="GET", endpoint=endpoint)
        self._handle_response(response)
        return response.json()

    def delete_tag_by_name(self, tag_name):
        logger.info(f"Deleting tag by name: {tag_name}")
        endpoint = config['tag_delete_by_name'].replace("{tag_name}", tag_name)
        response = self.client.make_request(method="DELETE", endpoint=endpoint)
        self._handle_response(response)
        return response.json()

    def add_tags_to_responses(self, tag_names, response_ids):
        data = {
            "tag_names": tag_names,
            "response_ids": response_ids
        }
        logger.info(f"Adding tags {tag_names} to responses {response_ids}")
        endpoint = config['tag_add_to_responses']  # Load from config
        response = self.client.make_request(method="POST", endpoint=endpoint, data=data)
        self._handle_response(response)
        return response.json()

    def remove_tags_from_responses(self, tag_names, response_ids):
        data = {
            "tag_names": tag_names,
            "response_ids": response_ids
        }
        logger.info(f"Removing tags {tag_names} from responses {response_ids}")
        endpoint = config['tag_remove_from_responses']
        response = self.client.make_request(method="POST", endpoint=endpoint, data=data)
        self._handle_response(response)
        return response.json()

    def add_tags_to_inputs(self, tag_names, input_ids):
        data = {
            "tag_names": tag_names,
            "input_ids": input_ids
        }
        logger.info(f"Adding tags {tag_names} to inputs {input_ids}")
        endpoint = config['tag_add_to_inputs']
        response = self.client.make_request(method="POST", endpoint=endpoint, data=data)
        self._handle_response(response)
        return response.json()

    def remove_tags_from_inputs(self, tag_names, input_ids):
        data = {
            "tag_names": tag_names,
            "input_ids": input_ids
        }
        logger.info(f"Removing tags {tag_names} from inputs {input_ids}")
        endpoint = config['tag_remove_from_inputs']
        response = self.client.make_request(method="POST", endpoint=endpoint, data=data)
        self._handle_response(response)
        if response.status_code == 204:
            return {'message': 'Tags removed successfully'}
        return response.json()

    def get_tags_by_type(self, tag_type):
        logger.info(f"Fetching tags by type: {tag_type}")
        endpoint = config['tag_get_by_type'].replace("{tag_type}", tag_type)
        response = self.client.make_request(method="GET", endpoint=endpoint)
        self._handle_response(response)
        return response.json()

    def get_tag_associations(self, tag_id):
        logger.info(f"Fetching tag associations for tag ID: {tag_id}")
        endpoint = config['tag_get_associations'].replace("{tag_id}", tag_id)
        response = self.client.make_request(method="GET", endpoint=endpoint)
        self._handle_response(response)
        return response.json()

    def _handle_response(self, response):
        if response is None:
            logger.error("Request failed: No response received.")
            raise EvaluableAIError("Request failed: No response received.")
        if response.status_code == 403:
            logger.error(f"Error 403: {response.json()}")
            raise PermissionDeniedError(
                response.json().get('message', 'Permission denied'),
                response=response,
                body=response.json()
            )
        elif response.status_code == 404:
            logger.error(f"Error 404: {response.json()}")
            raise NotFoundError(
                response.json().get('message', 'Resource not found'),
                response=response,
                body=response.json()
            )
        elif not response.is_success:
            logger.error(f"Error {response.status_code}: {response.json()}")
            if response.status_code == 204:
                return
            elif response.status_code == 400:
                logger.error(f"Validation errors: {response.json().get('errors', 'No detailed errors')}")
            raise APIStatusError(
                response.json().get('message', 'API request failed'),
                response=response,
                body=response.json()
            )
