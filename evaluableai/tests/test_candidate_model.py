import pytest
import os
import logging
from evaluableai.client import EvaluableAI
from evaluableai.objects.candidate_model import CandidateModel
from evaluableai.exceptions import EvaluableAIError

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

def test_create_candidate_model_success(client):
    """Test successful creation of a candidate model with real data."""
    candidate_model = CandidateModel(model_name="TestModelSaurav1", model_version="v5.1")

    try:
        response = candidate_model.create_candidate_model(client)
        candidate_model_id = response['data']['candidate_model']['candidate_model_id']
        assert candidate_model_id is not None, "Candidate model ID should not be None"
        logger.info("Successfully created candidate model with ID: %s", candidate_model_id)
    except Exception as e:
        pytest.fail(f"Failed to create candidate model: {e}")

def test_create_multiple_candidate_models_success(client):
    """Test successful creation of multiple candidate models with real data."""
    models = [
        CandidateModel(model_name="BulkModelSaurav1", model_version="v6.1"),
        CandidateModel(model_name="BulkModelSaurav2", model_version="v6.2")
    ]

    try:
        response = CandidateModel.create_multiple_candidate_models(client, models)
        assert response['success'], "Response should indicate success"
        assert 'candidate_models' in response['data'], "Response should contain candidate_models"
        for model in response['data']['candidate_models']:
            assert model['candidate_model_id'] is not None, "Each candidate model should have an ID"
        logger.info("Successfully created multiple candidate models")
    except Exception as e:
        pytest.fail(f"Failed to create multiple candidate models: {e}")

def test_update_candidate_model_success(client):
    """Test updating a candidate model with real data."""
    candidate_model = CandidateModel(model_name="UpdateTestModelSaurav1", model_version="v7.1")
    try:
        candidate_model.create_candidate_model(client)
        candidate_model.model_name = "UpdatedModelNameSaurav1"

        candidate_model_id = CandidateModel.find_candidate_model_id_by_name_and_version(client, "UpdateTestModelSaurav1", "v7.1")
        response = candidate_model.update_candidate_model(client, candidate_model_id)
        updated_name = response['data']['candidate_model']['model_name']
        assert updated_name == "UpdatedModelNameSaurav1", f"Expected model name to be UpdatedModelNameSaurav1, got {updated_name}"
        logger.info("Successfully updated candidate model to: %s", updated_name)
    except Exception as e:
        pytest.fail(f"Failed to update candidate model: {e}")

def test_get_candidate_model_by_id_success(client):
    """Test fetching a candidate model by ID with real data."""
    candidate_model = CandidateModel(model_name="FetchTestModelSaurav1", model_version="v8.1")
    try:
        candidate_model.create_candidate_model(client)
        candidate_model_id = CandidateModel.find_candidate_model_id_by_name_and_version(client, "FetchTestModelSaurav1", "v8.1")

        response = CandidateModel.get_candidate_model_by_id(client, candidate_model_id)
        fetched_id = response['data']['candidate_model']['candidate_model_id']
        assert fetched_id == candidate_model_id, f"Expected fetched ID to be {candidate_model_id}, got {fetched_id}"
        logger.info("Successfully fetched candidate model by ID: %s", fetched_id)
    except Exception as e:
        pytest.fail(f"Failed to fetch candidate model by ID: {e}")

def test_find_candidate_model_by_name_and_version(client):
    """Test finding a candidate model by name and version with real data."""
    candidate_model = CandidateModel(model_name="FindTestModelSaurav1", model_version="v9.1")
    try:
        candidate_model.create_candidate_model(client)

        response = CandidateModel.find_candidate_model_by_name_and_version(client, "FindTestModelSaurav1", "v9.1")
        model_name = response['data']['candidate_model']['model_name']
        assert model_name == "FindTestModelSaurav1", f"Expected model name to be FindTestModelSaurav1, got {model_name}"
        logger.info("Successfully found candidate model by name and version: %s", model_name)
    except Exception as e:
        pytest.fail(f"Failed to find candidate model by name and version: {e}")

def test_find_candidate_model_id_by_name_and_version(client):
    """Test finding a candidate model ID by name and version with real data."""
    candidate_model = CandidateModel(model_name="IDTestModelSaurav1", model_version="v10.1")
    try:
        candidate_model.create_candidate_model(client)

        candidate_model_id = CandidateModel.find_candidate_model_id_by_name_and_version(client, "IDTestModelSaurav1", "v10.1")
        assert candidate_model_id is not None, "Candidate model ID should not be None"
        logger.info("Successfully found candidate model ID: %s", candidate_model_id)
    except Exception as e:
        pytest.fail(f"Failed to find candidate model ID: {e}")
