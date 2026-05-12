import os
import pytest
import logging
from evaluableai.client import EvaluableAI
from evaluableai.objects.input import Input, InputVariables
from evaluableai.exceptions import PermissionDeniedError, NotFoundError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = EvaluableAI()

@pytest.fixture
def client():
    token = os.getenv("EVALUABLEAI_API_KEY")
    if not token:
        pytest.fail("EVALUABLEAI_API_KEY environment variable not set")
    return EvaluableAI(token=token)

def test_create_input_by_template_id_success(client):
    """Test successful creation of an input by template ID with real data."""
    input_client = Input(client)
    # Replace with your actual template ID
    template_id = "template-43a4d367-2bd5-4565-98dd-c833f17caf87"
    input_var = InputVariables(variables={"company": "TestCompany"}, expected_output="", metadata={"key": "value"})

    logger.info("Creating input by template ID...")
    response = input_client.create_input_by_template_id(template_id, input_var)
    assert response.success, "Input creation should be successful"
    assert "input" in response.data['data'], "Input data should be present in response"
    assert response.data['data']['input']['text'] == "Example prompt", "Text should match the template"
    logger.info("Create input by template ID response: %s", response.dict())

def test_create_many_input_by_template_id_success(client):
    """Test successful creation of multiple inputs by template ID with real data."""
    input_client = Input(client)
    # Replace with your actual template ID
    template_id = "template-43a4d367-2bd5-4565-98dd-c833f17caf87"
    inputs = [
        InputVariables(variables={"x": "LLM", "y": "Llama", "c": "abc"}, expected_output="", metadata={"key": "value"}),
        InputVariables(variables={"x": "Night", "y": "moon", "c": "def"}, expected_output="", metadata={"key": "value"}),
        InputVariables(variables={"x": "Day", "y": "sun", "c": "ghi"}, expected_output="", metadata={"key": "value"})
    ]

    logger.info("Creating multiple inputs by template ID...")
    response = input_client.create_many_input_by_template_id(template_id, inputs)
    assert response.success, "Multiple inputs creation should be successful"
    assert "inputs" in response.data['data'], "Inputs data should be present in response"
    assert len(response.data['data']['inputs']) == 3, "There should be three inputs created"
    logger.info("Create many inputs by template ID response: %s", response.dict())

def test_create_input_by_prompt_success(client):
    """Test successful creation of an input by prompt with real data."""
    input_client = Input(client)
    text = "Example prompt Saurav"
    context = "Example context"
    input_var = InputVariables(variables={"x": "ExampleX", "y": "ExampleY"}, expected_output="", metadata={"key": "value"})

    logger.info("Creating input by prompt...")
    response = input_client.create_input_by_template_prompt(text, context, input_var, "ExampleTemplate45287")
    assert response.success, "Input creation by prompt should be successful"
    assert "input" in response.data['data'], "Input data should be present in response"
    assert response.data['data']['input']['text'] == text, "Text should match the input text"
    logger.info("Create input by prompt response: %s", response.dict())

def test_create_many_inputs_by_prompt_success(client):
    """Test successful creation of multiple inputs by prompt with real data."""
    input_client = Input(client)
    text = "Example prompt Saurav1"
    context = "Example context"
    inputs = [
        InputVariables(variables={"x": "LLM", "y": "Llama", "c": "abc"}, expected_output="", metadata={"key": "value"}),
        InputVariables(variables={"x": "Night", "y": "moon", "c": "def"}, expected_output="", metadata={"key": "value"}),
        InputVariables(variables={"x": "Day", "y": "sun", "c": "ghi"}, expected_output="", metadata={"key": "value"})
    ]

    logger.info("Creating multiple inputs by prompt...")
    response = input_client.create_many_inputs_by_template_prompt(text, context, inputs, "ExampleTemplate46832")
    assert response.success, "Multiple inputs creation by prompt should be successful"
    assert "inputs" in response.data['data'], "Inputs data should be present in response"
    assert len(response.data['data']['inputs']) == 3, "There should be three inputs created"
    logger.info("Create many inputs by prompt response: %s", response.dict())

def test_create_input_by_openai_success(client):
    """Test successful creation of an input by OpenAI messages with real data."""
    input_client = Input(client)
    openai_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the weather like today?"},
        {"role": "assistant", "content": "The weather is sunny with a high of 25°C."}
    ]
    template_name = "OpenAI Template42641"
    expected_output = "Sunny weather forecast"

    logger.info("Creating input by OpenAI...")
    response = input_client.create_input_by_openai(
        messages=openai_messages,
        template_name=template_name,
        expected_output=expected_output,
        metadata={"source": "OpenAI"}
    )
    assert response.success, "Input creation by OpenAI should be successful"
    assert "input" in response.data['data'], "Input data should be present in response"
    assert response.data['data']['input']['expected_output'] == expected_output, "Expected output should match"
    logger.info("Create input by OpenAI response: %s", response.dict())

def test_create_input_by_template_id_not_found(client):
    """Test creating an input by template ID with a non-existent template."""
    input_client = Input(client)
    # Replace with a non-existent template ID for testing
    template_id = "non-existent-template-id"
    input_var = InputVariables(variables={"company": "TestCompany"}, expected_output="", metadata={"key": "value"})

    logger.info("Testing input creation with non-existent template ID...")
    response = input_client.create_input_by_template_id(template_id, input_var)
    assert not response.success, "Input creation should fail for non-existent template"
    assert response.status_code == 404, "Status code should be 404 for not found"
    logger.info("Create input by template ID with non-existent template response: %s", response.dict())

def test_create_many_input_by_template_id_permission_denied(client):
    """Test creating multiple inputs by template ID with an invalid token."""
    invalid_client = EvaluableAI(token="invalid-token")
    input_client = Input(invalid_client)
    # Replace with your actual template ID
    template_id = "template-43a4d367-2bd5-4565-98dd-c833f17caf87"
    inputs = [
        InputVariables(variables={"x": "LLM", "y": "Llama", "c": "abc"}, expected_output="", metadata={"key": "value"}),
        InputVariables(variables={"x": "Night", "y": "moon", "c": "def"}, expected_output="", metadata={"key": "value"}),
        InputVariables(variables={"x": "Day", "y": "sun", "c": "ghi"}, expected_output="", metadata={"key": "value"})
    ]

    logger.info("Testing input creation with invalid token...")
    response = input_client.create_many_input_by_template_id(template_id, inputs)
    assert not response.success, "Input creation should fail with invalid token"
    assert response.status_code == 403, "Status code should be 403 for permission denied"
    logger.info("Create many inputs by template ID with invalid token response: %s", response.dict())
