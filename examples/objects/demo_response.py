import os
import json
import logging
from evaluableai.client import EvaluableAI
from evaluableai.objects.response import Response
from evaluableai.exceptions import EvaluableAIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetching the API key from the environment variables and initializing the EvaluableAI client
token = os.getenv("EVALUABLEAI_API_KEY")
client = EvaluableAI(token)

# Example data for /response/create_1 (OpenAI response blob)
openai_data = {
    "candidate_model": {
        "name": "OPENAI",
        "version": "gpt-4"
    },
    "input": {
        "text": "What is black?"
    },
    "response": {
        "openai_response": {
            "model": "gpt-3.5-turbo-0125",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Black is a color."
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 9,
                "completion_tokens": 12,
                "total_tokens": 21
            }
        }
    }
}

def create_response_from_openai(client, data):
    logger.info("Creating response from OpenAI response blob.")
    try:
        # No need to pass the endpoint directly anymore, it is handled by the Response class via load_config()
        response_data = Response.create_response(client, data)
        response_id = response_data['data']['response']['id']
        logger.info("Created response:\n%s", json.dumps(response_data, indent=4))
        return response_id
    except EvaluableAIError as e:
        logger.error(f"Failed to create response: {e}")
        return None

def fetch_response_by_id(client, response_id):
    logger.info("Fetching response by ID: %s", response_id)
    try:
        response_data = Response.get_response_by_id(client, response_id)
        logger.info("Fetched response:\n%s", json.dumps(response_data, indent=4))
    except EvaluableAIError as e:
        logger.error(f"Failed to fetch response: {e}")

def delete_response_by_id(client, response_id):
    logger.info("Deleting response by ID: %s", response_id)
    try:
        response_data = Response.delete_response_by_id(client, response_id)
        logger.info("Deleted response:\n%s", json.dumps(response_data, indent=4))
    except EvaluableAIError as e:
        logger.error(f"Failed to delete response: {e}")

if __name__ == "__main__":
    # Step 1: Create a response from an OpenAI response blob
    response_id = create_response_from_openai(client, openai_data)

    if response_id:
        # Step 2: Fetch the created response by ID
        fetch_response_by_id(client, response_id)

        # Step 3: Delete the created response by ID
        delete_response_by_id(client, response_id)

    logger.info("Process completed.")
