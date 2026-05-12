import os
import json
import logging
from evaluableai.client import EvaluableAI
from evaluableai.objects.candidate_model import CandidateModel
from evaluableai.exceptions import EvaluableAIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch the API key from the environment variables and initialize the EvaluableAI client
valid_token = os.getenv("EVALUABLEAI_API_KEY")
client = EvaluableAI(valid_token)

# Define candidate models to be used in the script
candidate_model = CandidateModel(
    model_name="MyModel41",
    model_version="v4.0"
)

# Define multiple candidate models for bulk operations
models = [
    CandidateModel(
        model_name="TestModel11",
        model_version="v1.0",
        model_properties={
            "property1": "value1",
            "property2": 1234,
            "property3": True
        }
    ),
    CandidateModel(
        model_name="TestModel21",
        model_version="v1.1",
        model_properties={
            "property1": "value3",
            "property2": 5678,
            "property3": False
        }
    )
]

def main():
    # Create a single candidate model
    try:
        response = candidate_model.create_candidate_model(client)
        candidate_model_id = response['data']['candidate_model']['candidate_model_id']
        logger.info("Create Single candidate model response:\n%s", json.dumps(response, indent=4))
    except EvaluableAIError as e:
        logger.error(f"Error creating candidate model: {e}")
        return

    # Create multiple candidate models
    try:
        response = CandidateModel.create_multiple_candidate_models(client, models)
        logger.info("Create multiple candidate models response:\n%s", json.dumps(response, indent=4))
    except EvaluableAIError as e:
        logger.error(f"Error creating multiple candidate models: {e}")
        return

    # Update the created candidate model
    candidate_model.model_name = "UpdatedModelName"
    try:
        response = candidate_model.update_candidate_model(client, candidate_model_id)
        logger.info("Update candidate model response:\n%s", json.dumps(response, indent=4))
    except EvaluableAIError as e:
        logger.error(f"Error updating candidate model: {e}")
        return

    # Get the created candidate model by ID
    try:
        response = CandidateModel.get_candidate_model_by_id(client, candidate_model_id)
        logger.info("Get candidate model by ID response:\n%s", json.dumps(response, indent=4))
    except EvaluableAIError as e:
        logger.error(f"Error fetching candidate model: {e}")
        return

    # Find candidate model by name and version
    try:
        response = CandidateModel.find_candidate_model_by_name_and_version(client, "MyModel41", "v4.0")
        logger.info("Find candidate model by name and version response:\n%s", json.dumps(response, indent=4))
    except EvaluableAIError as e:
        logger.error(f"Error finding candidate model: {e}")
        return

    # Find candidate model ID by name and version
    try:
        candidate_model_id = CandidateModel.find_candidate_model_id_by_name_and_version(client, "MyModel41", "v4.0")
        logger.info("Candidate Model ID: %s", candidate_model_id)
    except EvaluableAIError as e:
        logger.error(f"Error finding candidate model ID: {e}")

if __name__ == "__main__":
    main()
    logger.info("Process completed.")
