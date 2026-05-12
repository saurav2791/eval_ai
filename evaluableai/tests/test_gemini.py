import os
import pytest
import logging
from evaluableai.gemini.gemini_overloader import CustomGenerativeModel
from evaluableai.exceptions import EvaluableAIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Parameters for the EvaluableAI model
evaluableai_token = os.getenv("EVALUABLEAI_API_KEY")

evaluableai_params = {
    "token": evaluableai_token,
    "eval": False,
    "sampling": 1,
    "eval_list": ["Sentiment"],
    "async": True,
    "tag_names": ["EXP 1", "Open AI"],
    "model_name": "gemini-1.0-pro-latest"
}

fact_questions_with_answers = [
    ["What is the only mammal capable of true flight?", "Bats"],
    ["In what year did Neil Armstrong and Buzz Aldrin land on the moon?", "1969"],
]

@pytest.fixture
def custom_model():
    """Fixture to initialize the CustomGenerativeModel."""
    return CustomGenerativeModel(evaluableai_params=evaluableai_params)

# Initialization Tests
def test_initialization_with_valid_api_key(custom_model):
    """Test that the model initializes correctly with a valid API key."""
    assert custom_model is not None, "Model should be initialized"
    logger.info("Model initialized successfully with valid API key.")

def test_initialization_with_missing_api_key():
    """Test that initialization fails without an API key."""
    with pytest.raises(ValueError, match="API_KEY must be provided"):
        CustomGenerativeModel(evaluableai_params={"token": evaluableai_token, "model_name": "gemini-1.0-pro-latest"})
    logger.info("Initialization failed as expected due to missing API key.")

def test_initialization_with_missing_evaluableai_token():
    """Test that initialization fails without an Evaluable AI token."""
    with pytest.raises(KeyError):
        CustomGenerativeModel(evaluableai_params={"model_name": "gemini-1.0-pro-latest"}, API_KEY="VALID_API_KEY")
    logger.info("Initialization failed as expected due to missing EvaluableAI token.")

# Synchronous Content Generation Tests
def test_generate_content_real(custom_model):
    """Test generating content with real data."""
    for question, ground_truth in fact_questions_with_answers:
        response = custom_model.generate_content(
            contents=[{"role": "user", "parts": [{"text": question}]}],
            ground_truth=ground_truth
        )
        result = response.candidates[0].content.parts[0].text
        assert result is not None, f"Response should not be empty for question: {question}"
        logger.info("Generated content successfully for question: %s", question)

def test_generate_content_with_empty_contents(custom_model):
    """Test that generating content fails with empty contents."""
    with pytest.raises(TypeError):
        custom_model.generate_content(contents=[])
    logger.info("Content generation failed as expected due to empty contents.")

def test_generate_content_with_missing_parameters(custom_model):
    """Test that generating content fails with missing parameters."""
    with pytest.raises(TypeError):
        custom_model.generate_content()
    logger.info("Content generation failed as expected due to missing parameters.")

# Asynchronous Content Generation Tests
@pytest.mark.asyncio
async def test_generate_content_async_real(custom_model):
    """Test generating content asynchronously with real data."""
    for question, ground_truth in fact_questions_with_answers:
        response = await custom_model.generate_content_async(
            contents=[{"role": "user", "parts": [{"text": question}]}],
            ground_truth=ground_truth
        )
        result = response.candidates[0].content.parts[0].text
        assert result is not None, f"Response should not be empty for question: {question}"
        logger.info("Generated content asynchronously successfully for question: %s", question)

@pytest.mark.asyncio
async def test_generate_content_async_with_empty_contents(custom_model):
    """Test that generating content asynchronously fails with empty contents."""
    with pytest.raises(TypeError):
        await custom_model.generate_content_async(contents=[])
    logger.info("Asynchronous content generation failed as expected due to empty contents.")

@pytest.mark.asyncio
async def test_generate_content_async_with_missing_parameters(custom_model):
    """Test that generating content asynchronously fails with missing parameters."""
    with pytest.raises(TypeError):
        await custom_model.generate_content_async()
    logger.info("Asynchronous content generation failed as expected due to missing parameters.")

# Error Handling Tests
def test_handling_of_invalid_api_key():
    """Test error handling with an invalid API key."""
    invalid_params = evaluableai_params.copy()
    invalid_params["token"] = "INVALID_TOKEN"
    invalid_model = CustomGenerativeModel(evaluableai_params=invalid_params)
    with pytest.raises(EvaluableAIError):
        invalid_model.generate_content(
            contents=[{"role": "user", "parts": [{"text": "Test"}]}]
        )
    logger.info("Error handling worked as expected for invalid API key.")

@pytest.mark.asyncio
async def test_handling_of_network_errors():
    """Test error handling during network errors."""
    invalid_params = evaluableai_params.copy()
    invalid_params["token"] = "INVALID_TOKEN"
    invalid_model = CustomGenerativeModel(evaluableai_params=invalid_params)
    with pytest.raises(EvaluableAIError):
        await invalid_model.generate_content_async(
            contents=[{"role": "user", "parts": [{"text": "Test"}]}]
        )
    logger.info("Error handling worked as expected during network errors.")

if __name__ == "__main__":
    pytest.main()
