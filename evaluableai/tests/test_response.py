import pytest
import os
import json
import logging
from evaluableai.client import EvaluableAI
from evaluableai.objects.response import Response
from evaluableai.exceptions import (
    BadRequestError,
    PermissionDeniedError,
    NotFoundError,
    APIStatusError
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def client():
    """Fixture to create an EvaluableAI client with a real token."""
    token = os.getenv("EVALUABLEAI_API_KEY")
    if not token:
        pytest.fail("EVALUABLEAI_API_KEY environment variable not set")
    return EvaluableAI(token=token)

def test_create_response_success(client):
    """Test successful creation of a response with real data."""
    data = {
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

    try:
        response_data = Response.create_response(client, "/response/create_1", data)
        assert response_data['data']['response']['id'] is not None
        logger.info("Created response: %s", json.dumps(response_data, indent=4))
    except Exception as e:
        pytest.fail(f"Failed to create response: {e}")

def test_create_response_missing_fields(client):
    """Test creating a response with missing required fields."""
    data = {
        "candidate_model": {
            "name": "OPENAI"
            # Missing version field
        },
        "input": {
            "text": "What is black?"
        }
        # Missing response field
    }

    with pytest.raises(BadRequestError):
        Response.create_response(client, "/response/create_1", data)

def test_create_response_invalid_model(client):
    """Test creating a response with an invalid candidate model."""
    data = {
        "candidate_model": {
            "name": "INVALID_MODEL",
            "version": "v1"
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

    with pytest.raises(BadRequestError):
        Response.create_response(client, "/response/create_1", data)

def test_get_response_invalid_id(client):
    """Test fetching a response with an invalid ID."""
    invalid_response_id = "invalid-id"

    with pytest.raises(NotFoundError):
        Response.get_response_by_id(client, invalid_response_id)

def test_delete_response_invalid_id(client):
    """Test deleting a response with an invalid ID."""
    invalid_response_id = "invalid-id"

    with pytest.raises(NotFoundError):
        Response.delete_response_by_id(client, invalid_response_id)

def test_create_response_invalid_token():
    """Test creating a response with an invalid API token."""
    client = EvaluableAI(token="invalid-token")
    data = {
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

    with pytest.raises(PermissionDeniedError):
        Response.create_response(client, "/response/create_1", data)

def test_create_response_with_different_content_types(client):
    """Test creating a response with different content types."""
    data = {
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
                            "content": "Here is an image of black."
                        },
                        "image_url": "https://example.com/image.jpg"
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

    try:
        response_data = Response.create_response(client, "/response/create_1", data)
        assert response_data['data']['response']['id'] is not None
        logger.info("Created response with different content types: %s", json.dumps(response_data, indent=4))
    except Exception as e:
        pytest.fail(f"Failed to create response with different content types: {e}")

def test_get_response_by_id_success(client):
    """Test fetching a response by ID with real data."""
    # First, create a response to get a valid ID
    data = {
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

    response_data = Response.create_response(client, "/response/create_1", data)
    response_id = response_data['data']['response']['id']

    try:
        fetched_response_data = Response.get_response_by_id(client, response_id)
        assert fetched_response_data['data']['response']['id'] == response_id
        logger.info("Fetched response by ID: %s", json.dumps(fetched_response_data, indent=4))
    except Exception as e:
        pytest.fail(f"Failed to fetch response by ID: {e}")

def test_delete_response_by_id_success(client):
    """Test deleting a response by ID with real data."""
    # First, create a response to get a valid ID
    data = {
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

    response_data = Response.create_response(client, "/response/create_1", data)
    response_id = response_data['data']['response']['id']

    try:
        delete_response_data = Response.delete_response_by_id(client, response_id)
        assert delete_response_data['message'] == "Response is successfully deleted."
        logger.info("Deleted response by ID: %s", json.dumps(delete_response_data, indent=4))
    except Exception as e:
        pytest.fail(f"Failed to delete response by ID: {e}")
