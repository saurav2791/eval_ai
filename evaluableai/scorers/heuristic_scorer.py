import yaml
import os
import json
import logging
from evaluableai.client import EvaluableAI


def load_config() -> dict:
    """
    Load the endpoint configuration from the endpoint.json file located in the evaluableai directory.

    :return: A dictionary with the endpoint mappings.
    """
    # Get the directory path of the current module (evaluableai/scorers)
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


class HeuristicScorer:
    def __init__(self, client: EvaluableAI):
        self.client = client

    def load_yaml_file(self, filename: str) -> dict:
        """
        Load a YAML file from the config folder located in the Scorer directory.

        :param filename: The name of the YAML file to load.
        :return: The content of the YAML file as a dictionary.
        """
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_folder = os.path.join(current_dir, 'config')
            file_path = os.path.join(config_folder, filename)

            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
                logging.info(f"YAML file '{filename}' loaded successfully.")
                return data
        except FileNotFoundError:
            logging.error(f"YAML file '{filename}' not found in '{config_folder}'.")
            raise
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file '{filename}': {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error loading YAML file '{filename}': {e}")
            raise

    def create_scorer_from_yaml(self, yaml_filename: str) -> dict:
        """
        Create a Heuristic Scorer using a YAML configuration file.

        :param yaml_filename: The name of the YAML file to use for creating the scorer.
        :return: The created scorer's details.
        """
        scorer_data = self.load_yaml_file(yaml_filename)
        return self.create_scorer(scorer_data)

    def create_scorer(self, scorer_data: dict) -> dict:
        """
        Creates a new Heuristic Scorer.

        :param scorer_data: A dictionary containing the scorer's details.
        :return: The created scorer's details.
        """
        try:
            # Load the endpoint dynamically from the config
            endpoint = config['heuristic_create']  # Load from config
            response = self.client.make_request(
                method="POST",
                endpoint=endpoint,  # Use the dynamically loaded endpoint
                data=scorer_data
            )
            logging.info("Heuristic scorer created successfully.")
            return response.json()
        except Exception as e:
            logging.error(f"Error creating scorer: {e}")
            raise

    def update_scorer(self, scorer_id: str, scorer_data: dict) -> dict:
        """
        Updates an existing Heuristic Scorer.

        :param scorer_id: The ID of the scorer to update.
        :param scorer_data: A dictionary containing the updated scorer's details.
        :return: The updated scorer's details.
        """
        try:
            # Load the endpoint dynamically from the config
            endpoint = config['heuristic_update']  # Load from config
            response = self.client.make_request(
                method="PUT",
                endpoint=endpoint,
                data=scorer_data
            )
            logging.info(f"Heuristic scorer '{scorer_id}' updated successfully.")
            return response.json()
        except Exception as e:
            logging.error(f"Error updating scorer '{scorer_id}': {e}")
            raise

    def get_scorer_by_id(self, scorer_id: str) -> dict:
        """
        Retrieve a Heuristic Scorer by its ID.

        :param scorer_id: The ID of the scorer to retrieve.
        :return: The scorer's details.
        """
        try:
            # Load the endpoint dynamically from the config
            endpoint = config['heuristic_get_by_id'].replace("{scorer_id}", scorer_id)  # Replace dynamic part
            response = self.client.make_request(
                method="GET",
                endpoint=endpoint
            )
            logging.info(f"Retrieved scorer by ID '{scorer_id}'.")
            return response.json()
        except Exception as e:
            logging.error(f"Error retrieving scorer by ID '{scorer_id}': {e}")
            raise

    def get_scorer_by_name(self, scorer_name: str) -> dict:
        """
        Retrieve a Heuristic Scorer by its name.

        :param scorer_name: The name of the scorer to retrieve.
        :return: The scorer's details.
        """
        try:
            # Load the endpoint dynamically from the config
            endpoint = config['heuristic_get_by_name'].replace("{scorer_name}", scorer_name)  # Replace dynamic part
            response = self.client.make_request(
                method="GET",
                endpoint=endpoint
            )
            logging.info(f"Retrieved scorer by name '{scorer_name}'.")
            return response.json()
        except Exception as e:
            logging.error(f"Error retrieving scorer by name '{scorer_name}': {e}")
            raise

    def get_scorers(self) -> list:
        """
        Retrieves all Heuristic Scorers.

        :return: A list of all scorers.
        """
        try:
            # Load the endpoint dynamically from the config
            endpoint = config['heuristic_get_all']  # Load from config
            response = self.client.make_request(
                method="GET",
                endpoint=endpoint
            )
            logging.info("Retrieved all heuristic scorers.")
            return response.json()
        except Exception as e:
            logging.error(f"Error fetching all scorers: {e}")
            raise

    def delete_scorer(self, scorer_id: str) -> dict:
        """
        Deletes a Heuristic Scorer by ID.

        :param scorer_id: The ID of the scorer to be deleted.
        :return: Confirmation message of the deletion.
        """
        try:
            # Load the endpoint dynamically from the config
            endpoint = config['heuristic_delete_by_id'].replace("{scorer_id}", scorer_id)  # Replace dynamic part
            response = self.client.make_request(
                method="DELETE",
                endpoint=endpoint
            )
            logging.info(f"Deleted heuristic scorer with ID '{scorer_id}'.")
            return response.json()
        except Exception as e:
            logging.error(f"Error deleting scorer '{scorer_id}': {e}")
            raise
