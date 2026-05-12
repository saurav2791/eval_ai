import json
import logging
import httpx
import os
from dataclasses import dataclass, field
from typing import List, Dict, Any
from evaluableai.client import EvaluableAI
from evaluableai.exceptions import (
    BadRequestError,
    PermissionDeniedError,
    NotFoundError,
    APIStatusError
)

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
class CandidateModel:
    model_name: str
    model_version: str
    model_properties: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def handle_response(response: httpx.Response) -> Dict[str, Any]:
        if response.status_code in {200, 201}:
            return response.json()
        elif response.status_code == 400:
            logger.error("Bad Request: %s", response.json())
            raise BadRequestError(message="Bad Request", response=response, body=response.json())
        elif response.status_code == 403:
            logger.error("Permission Denied: %s", response.json())
            raise PermissionDeniedError(message="Forbidden", response=response, body=response.json())
        elif response.status_code == 404:
            logger.error("Not Found: %s", response.json())
            raise NotFoundError(message="Not Found", response=response, body=response.json())
        else:
            logger.error("Unexpected Status Code %d: %s", response.status_code, response.text)
            raise APIStatusError(message=f"Error {response.status_code}", response=response, body=response.json())

    def create_candidate_model(self, client: EvaluableAI) -> Dict[str, Any]:
        url = config['candidate_model_create']  # Load endpoint from config
        data = {
            "model_name": self.model_name,
            "model_version": self.model_version,
            "model_properties": self.model_properties
        }
        logger.info("Creating candidate model: %s, version: %s", self.model_name, self.model_version)
        response = client.make_request(method="POST", endpoint=url, data=data)
        return self.handle_response(response)

    @classmethod
    def create_multiple_candidate_models(cls, client: EvaluableAI, models: List['CandidateModel']) -> Dict[str, Any]:
        url = config['candidate_model_bulk_create']  # Load endpoint from config
        data = {
            "candidate_models": [
                {
                    "model_name": model.model_name,
                    "model_version": model.model_version,
                    "model_properties": model.model_properties
                }
                for model in models
            ]
        }
        logger.info("Creating multiple candidate models.")
        response = client.make_request(method="POST", endpoint=url, data=data)
        return cls.handle_response(response)

    def update_candidate_model(self, client: EvaluableAI, candidate_model_id: str) -> Dict[str, Any]:
        url = config['candidate_model_update'].replace("{candidate_model_id}", candidate_model_id)  # Load endpoint from config
        data = {
            "model_name": self.model_name,
            "model_version": self.model_version,
            "model_properties": self.model_properties
        }
        logger.info("Updating candidate model ID: %s", candidate_model_id)
        response = client.make_request(method="PUT", endpoint=url, data=data)
        return self.handle_response(response)

    @classmethod
    def get_candidate_model_by_id(cls, client: EvaluableAI, candidate_model_id: str) -> Dict[str, Any]:
        url = config['candidate_model_get_by_id'].replace("{candidate_model_id}", candidate_model_id)  # Load endpoint from config
        logger.info("Fetching candidate model by ID: %s", candidate_model_id)
        response = client.make_request(method="GET", endpoint=url)
        return cls.handle_response(response)

    @classmethod
    def find_candidate_model_by_name_and_version(cls, client: EvaluableAI, model_name: str, model_version: str) -> Dict[str, Any]:
        url = config['candidate_model_find_by_name_and_version'].replace("{model_name}", model_name).replace("{model_version}", model_version)  # Load endpoint from config
        logger.info("Finding candidate model by name: %s and version: %s", model_name, model_version)
        response = client.make_request(method="GET", endpoint=url)
        return cls.handle_response(response)

    @classmethod
    def find_candidate_model_id_by_name_and_version(cls, client: EvaluableAI, model_name: str, model_version: str) -> str:
        logger.info("Finding candidate model ID by name: %s and version: %s", model_name, model_version)
        response = cls.find_candidate_model_by_name_and_version(client, model_name, model_version)
        if response.get('success'):
            candidate_model_id = response['data']['candidate_model']['candidate_model_id']
            return candidate_model_id
        else:
            logger.error("Candidate model with name %s and version %s not found.", model_name, model_version)
            raise NotFoundError(f"Candidate model with name {model_name} and version {model_version} not found.")
