import yaml
import os
import json
import logging
from evaluableai.client import EvaluableAI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config() -> dict:
    """
    Load the endpoint configuration from the endpoint.json file located in the evaluableai directory.

    :return: A dictionary with the endpoint mappings.
    """
    # Get the directory path of the current module
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(current_dir, '..', 'endpoint.json')
    # Normalize the path
    config_file = os.path.normpath(config_file)
    # Now try to open and load the config file
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found at: {config_file}")

    with open(config_file, 'r') as f:
        return json.load(f)


# Load the endpoint configuration from endpoint.json
config = load_config()


class LLMScorer:
    def __init__(self, client: EvaluableAI):
        self.client = client

    def load_yaml_file(self, filename: str) -> dict:
        """
        Load a YAML file from the data folder located in the Scorer directory.

        :param filename: The name of the YAML file to load.
        :return: The content of the YAML file as a dictionary.
        :raises: FileNotFoundError if the file is not found.
        :raises: yaml.YAMLError if there is an error parsing the YAML file.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_folder = os.path.join(current_dir, 'data')
        file_path = os.path.join(config_folder, filename)

        try:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
                logger.info(f"Successfully loaded YAML file: {file_path}")
                return data
        except FileNotFoundError:
            logger.error(f"YAML file not found: {file_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading YAML file: {e}")
            raise

    def create_scorer_from_yaml(self, yaml_filename: str) -> dict:
        """
        Create an LLM Scorer using a YAML configuration file.

        :param yaml_filename: The name of the YAML file to use for creating the scorer.
        :return: The created scorer's details.
        :raises: Exception if there is an error creating the scorer.
        """
        scorer_data = self.load_yaml_file(yaml_filename)
        return self.create_scorer(scorer_data)

    def create_scorer(self, scorer_data: dict) -> dict:
        """
        Creates a new LLM Scorer.

        :param scorer_data: A dictionary containing the scorer's details.
        :return: The created scorer's details.
        :raises: Exception if there is an error creating the scorer.
        """
        try:
            # Load the endpoint dynamically from the config
            endpoint = config['llm_create']  # Load from config
            response = self.client.make_request(method="POST", endpoint=endpoint, data=scorer_data)
            response_data = response.json()
            logger.info("Successfully created LLM Scorer.")
            return response_data
        except Exception as e:
            logger.error(f"Error creating scorer: {e}")
            raise

    def get_scorer_by_id(self, scorer_id: str) -> dict:
        """
        Retrieve an LLM Scorer by its ID.

        :param scorer_id: The ID of the scorer to retrieve.
        :return: The scorer's details.
        :raises: Exception if there is an error retrieving the scorer.
        """
        try:
            # Load the endpoint dynamically from the config
            endpoint = config['llm_get_by_id'].replace("{scorer_id}", scorer_id)  # Replace dynamic part
            response = self.client.make_request(method="GET", endpoint=endpoint)
            response_data = response.json()
            logger.info(f"Successfully retrieved LLM Scorer by ID: {scorer_id}")
            return response_data
        except Exception as e:
            logger.error(f"Error retrieving scorer by ID: {e}")
            raise

    def get_scorer_by_name(self, scorer_name: str) -> dict:
        """
        Retrieve an LLM Scorer by its name.

        :param scorer_name: The name of the scorer to retrieve.
        :return: The scorer's details.
        :raises: Exception if there is an error retrieving the scorer.
        """
        try:
            # Load the endpoint dynamically from the config
            endpoint = config['llm_get_by_name'].replace("{scorer_name}", scorer_name)  # Replace dynamic part
            response = self.client.make_request(method="GET", endpoint=endpoint)
            response_data = response.json()
            logger.info(f"Successfully retrieved LLM Scorer by name: {scorer_name}")
            return response_data
        except Exception as e:
            logger.error(f"Error retrieving scorer by name: {e}")
            raise

    def get_scorers(self) -> list:
        """
        Retrieves all LLM Scorers.

        :return: A list of all scorers.
        :raises: Exception if there is an error fetching the scorers.
        """
        try:
            # Load the endpoint dynamically from the config
            endpoint = config['llm_get_all']  # Load from config
            response = self.client.make_request(method="GET", endpoint=endpoint)
            response_data = response.json()
            logger.info("Successfully retrieved all LLM Scorers.")
            return response_data
        except Exception as e:
            logger.error(f"Error fetching scorers: {e}")
            raise

    def delete_scorer(self, scorer_id: str) -> dict:
        """
        Deletes an LLM Scorer by ID.

        :param scorer_id: The ID of the scorer to be deleted.
        :return: Confirmation message of the deletion.
        :raises: Exception if there is an error deleting the scorer.
        """
        try:
            # Load the endpoint dynamically from the config
            endpoint = config['llm_delete_by_id'].replace("{scorer_id}", scorer_id)  # Replace dynamic part
            response = self.client.make_request(method="DELETE", endpoint=endpoint)
            response_data = response.json()
            logger.info(f"Successfully deleted LLM Scorer with ID: {scorer_id}")
            return response_data
        except Exception as e:
            logger.error(f"Error deleting scorer: {e}")
            raise
