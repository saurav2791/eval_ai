import os
import logging
from evaluableai.client import EvaluableAI
from evaluableai.objects.input import Input, InputVariables
from evaluableai.exceptions import EvaluableAIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the EvaluableAI client
client = EvaluableAI()

# The template we are using for this example has variables 'x', 'y', and 'c'.
inputs_for_multiple = [
    InputVariables(variables={"x": "Machine Learning", "y": "Neural Networks", "c": "advanced technology"},
                   expected_output="", metadata={"key": "example1"}),
    InputVariables(variables={"x": "Night", "y": "Stars", "c": "clear sky"}, expected_output="",
                   metadata={"key": "example2"}),
    InputVariables(variables={"x": "Morning", "y": "Sunrise", "c": "beautiful view"}, expected_output="",
                   metadata={"key": "example3"})
]

openai_messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Can you explain how neural networks work?"},
    {"role": "assistant",
     "content": "Neural networks are computing systems inspired by the human brain's network of neurons."}
]

template_id = "ADD_YOUR_TEMPLATE_ID_HERE"  # Replace with your actual template ID


def create_input_by_template_id(input_client, template_id):
    logger.info("--- Example 1: Create input by template ID ---")
    input_data = InputVariables(variables={"company": "TechCorp"}, expected_output="", metadata={"key": "example4"})
    try:
        response = input_client.create_input_by_template_id(template_id, input_data)
        logger.info("Create input by template ID:\n%s", response.dict())
    except EvaluableAIError as e:
        logger.error(f"Failed to create input by template ID: {e}")


def create_multiple_inputs_by_template_id(input_client, template_id):
    logger.info("--- Example 2: Create multiple inputs by template ID ---")
    try:
        response = input_client.create_many_input_by_template_id(template_id, inputs_for_multiple)
        logger.info("Create multiple inputs by template ID:\n%s", response.dict())
    except EvaluableAIError as e:
        logger.error(f"Failed to create multiple inputs by template ID: {e}")


def create_input_by_template_prompt(input_client):
    logger.info("--- Example 3: Create input by prompt ---")
    input_data = InputVariables(variables={"x": "Python", "y": "Django", "c": "popular web framework"},
                                expected_output="", metadata={"key": "example5"})
    try:
        response = input_client.create_input_by_template_prompt(
            text="What is {{x}} and how does it relate to {{y}}?",
            context="This context focuses on {{c}}.",
            input_data=input_data,
            template_name="Tech_Insights_Template"
        )
        logger.info("Create input by prompt:\n%s", response.dict())
    except EvaluableAIError as e:
        logger.error(f"Failed to create input by prompt: {e}")


def create_multiple_inputs_by_template_prompt(input_client):
    logger.info("--- Example 4: Create multiple inputs by prompt ---")
    try:
        response = input_client.create_many_inputs_by_template_prompt(
            prompt="Explain the concept of {{x}} and its relation to {{y}}.",
            context="The context is related to {{c}}.",
            inputs=inputs_for_multiple,
            template_name="Learning_Concepts_Template"
        )
        logger.info("Create multiple inputs by prompt:\n%s", response.dict())
    except EvaluableAIError as e:
        logger.error(f"Failed to create multiple inputs by prompt: {e}")


def create_input_by_openai(input_client):
    logger.info("--- Example 5: Create input using OpenAI messages ---")
    try:
        response = input_client.create_input_by_openai(
            messages=openai_messages,
            template_name="Neural_Networks_Explainer_Template",
            expected_output="Explanation of neural networks",
            metadata={"source": "OpenAI"}
        )
        logger.info("Create input by OpenAI:\n%s", response.dict())
    except EvaluableAIError as e:
        logger.error(f"Failed to create input by OpenAI: {e}")


if __name__ == "__main__":
    input_client = Input(client=client)

    # Example 1: Create input by template ID
    create_input_by_template_id(input_client, template_id)

    # Example 2: Create multiple inputs by template ID
    create_multiple_inputs_by_template_id(input_client, template_id)

    # Example 3: Create input by Template prompt
    create_input_by_template_prompt(input_client)

    # Example 4: Create multiple inputs by prompt
    create_multiple_inputs_by_template_prompt(input_client)

    # Example 5: Create input using OpenAI messages
    create_input_by_openai(input_client)

    logger.info("Process completed.")
