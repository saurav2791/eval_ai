import os
import uuid
import logging
import json
from typing import Dict, Any, List
from datetime import datetime, timezone
from dataclasses import dataclass, field
from evaluableai.client import EvaluableAI
from evaluableai.objects.template import Template
from evaluableai.exceptions import NotFoundError, APIStatusError, PermissionDeniedError

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
class InputVariables:
    variables: Dict[str, Any]
    expected_output: str = None
    metadata: Dict[str, Any] = None

@dataclass
class APIResponse:
    success: bool
    message: str
    data: dict = field(default_factory=dict)
    status_code: int = 200  # Default status code

    def dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data
        }


class Input:
    def __init__(self, client: EvaluableAI):
        self.client = client

    def get_template_by_id(self, template_id: str) -> Dict[str, Any]:
        try:
            logger.info(f"Fetching template with ID: {template_id}")
            template = Template(id=template_id)
            template_data = template.fetch()
            if not template_data:
                logger.error(f"Template with ID {template_id} not found.")
                raise NotFoundError(f"Template with ID {template_id} not found.")
            return template_data
        except NotFoundError as e:
            logger.exception(f"Template with ID {template_id} not found.")
            raise e
        except Exception as e:
            logger.exception(f"Failed to fetch template: {str(e)}")
            raise APIStatusError(f"Failed to fetch template: {str(e)}")

    def create_input(self, template_data: Dict[str, Any], input_data: InputVariables) -> Dict[str, Any]:
        prompt = template_data.get("prompt")
        context = template_data.get("context", "")

        if not prompt:
            logger.error("Template prompt is missing.")
            raise ValueError("Template prompt is missing")

        text = prompt.format(**input_data.variables)
        context = context.format(**input_data.variables) if context else ""

        return {
            "id": str(uuid.uuid4()),
            "text": text,
            "context": context,
            "expected_output": input_data.expected_output,
            "metadata": input_data.metadata,
            "variables": input_data.variables,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

    def create_input_by_template_id(self, template_id: str, input_data: InputVariables) -> APIResponse:
        try:
            template_data = self.get_template_by_id(template_id)
            input_data_dict = self.create_input(template_data, input_data)

            endpoint = config['input_create_by_template_id']  # Load from config
            payload = {
                "template_id": template_id,
                "input": input_data_dict
            }

            response = self.client.make_request(method="POST", endpoint=endpoint, data=payload)
            return self._handle_response(response)

        except Exception as e:
            logger.exception(f"Failed to create input by template ID: {str(e)}")
            return APIResponse(success=False, message=str(e))

    def create_many_input_by_template_id(self, template_id: str, inputs: List[InputVariables]) -> APIResponse:
        try:
            template_data = self.get_template_by_id(template_id)
            inputs_data = [self.create_input(template_data, input_data) for input_data in inputs]

            endpoint = config['input_create_many_by_template_id']  # Load from config
            payload = {
                "template_id": template_id,
                "inputs": inputs_data
            }

            response = self.client.make_request(method="POST", endpoint=endpoint, data=payload)
            return self._handle_response(response)

        except Exception as e:
            logger.exception(f"Failed to create multiple inputs by template ID: {str(e)}")
            return APIResponse(success=False, message=str(e))

    def create_input_by_template_prompt(self, text: str, context: str, input_data: InputVariables, template_name: str = None) -> APIResponse:
        try:
            endpoint = config['input_create_by_prompt']  # Load from config
            payload = {
                "text": text,
                "context": context,
                "template_name": template_name,
                "input": {
                    "variables": input_data.variables,
                    "expected_output": input_data.expected_output,
                    "metadata": input_data.metadata,
                }
            }
            response = self.client.make_request(method="POST", endpoint=endpoint, data=payload)
            return self._handle_response(response)

        except Exception as e:
            logger.exception(f"Failed to create input by template prompt: {str(e)}")
            return APIResponse(success=False, message=str(e))

    def create_many_inputs_by_template_prompt(self, prompt: str, context: str, inputs: List[InputVariables], template_name: str = None) -> APIResponse:
        try:
            endpoint = config['input_create_many_by_prompt']  # Load from config
            payload = {
                "text": prompt,
                "context": context,
                "template_name": template_name,
                "inputs": [
                    {
                        "variables": input_data.variables,
                        "expected_output": input_data.expected_output,
                        "metadata": input_data.metadata,
                    } for input_data in inputs
                ]
            }
            response = self.client.make_request(method="POST", endpoint=endpoint, data=payload)
            return self._handle_response(response)

        except Exception as e:
            logger.exception(f"Failed to create multiple inputs by template prompt: {str(e)}")
            return APIResponse(success=False, message=str(e))

    def create_input_by_openai(self, messages: List[Dict[str, Any]], template_name: str = None, expected_output: str = "", metadata: Dict[str, Any] = None) -> APIResponse:
        try:
            endpoint = config['input_create_by_openai']  # Load from config
            payload = {
                "messages": messages,
                "template_name": template_name if template_name else str(uuid.uuid4()),
                "expected_output": expected_output,
                "metadata": metadata or {}
            }
            response = self.client.make_request(method="POST", endpoint=endpoint, data=payload)
            return self._handle_response(response)

        except Exception as e:
            logger.exception(f"Failed to create input by OpenAI: {str(e)}")
            return APIResponse(success=False, message=str(e))

    def _handle_response(self, response) -> APIResponse:
        if response is None:
            logger.error("Request failed: No response received.")
            raise APIStatusError("Request failed: No response received.")
        if response.status_code in {200, 201}:
            return APIResponse(success=True, message="Operation successful", data=response.json())
        elif response.status_code == 403:
            logger.error(f"Permission denied: {response.json()}")
            raise PermissionDeniedError(response.json().get('message', 'Permission denied'))
        elif response.status_code == 404:
            logger.error(f"Resource not found: {response.json()}")
            raise NotFoundError(response.json().get('message', 'Resource not found'))
        else:
            logger.error(f"Request failed with status code {response.status_code}: {response.text}")
            raise APIStatusError(f"Request failed with status code {response.status_code}: {response.text}")
