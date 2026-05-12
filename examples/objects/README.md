
# EvaluableAI SDK

This SDK provides classes for interacting with the EvaluableAI API, specifically focusing on managing inputs, candidate models, responses, and tags. Below is the documentation for the key components: `Input`, `CandidateModel`, `Response`, and `Tag`.

## Table of Contents

1. [Input](#input)
   - [Methods](#input-methods)
   - [Examples](#input-examples)
2. [CandidateModel](#candidate-model)
   - [Methods](#candidate-model-methods)
   - [Examples](#candidate-model-examples)
3. [Response](#response)
   - [Methods](#response-methods)
   - [Examples](#response-examples)
4. [Tag](#tag-management)
   - [Setup](#setup)
   - [Methods](#tag-methods)
   - [Examples](#tag-examples)

## Input

The `Input` class allows you to create and manage input objects linked to templates. You can create inputs by template ID, prompt, or using OpenAI messages.

### Input Methods

- **create_input_by_template_id**  
  Creates an input using a template ID.

- **create_many_input_by_template_id**  
  Creates multiple inputs using a template ID.

- **create_input_by_prompt**  
  Creates an input using a prompt and context.

- **create_many_inputs_by_prompt**  
  Creates multiple inputs using a prompt and context.

- **create_input_by_openai**  
  Creates an input using OpenAI messages.

### Input Examples

```python
from evaluableai.client import EvaluableAI
from evaluableai.objects.input import Input, InputVariables

client = EvaluableAI()
input_client = Input(client=client)

# Example: Create input by template ID
input_data = InputVariables(variables={"company": "TestCompany"}, expected_output="", metadata={"key": "value"})
template_id = "template-43a4d367-2bd5-4565-98dd-c833f17caf87"
response = input_client.create_input_by_template_id(template_id, input_data)
print("Create input by template ID:", response.dict())

# Example: Create input by prompt
input_data = InputVariables(variables={"x": "JAVA", "y": "Llama", "c": "abc"}, expected_output="", metadata={"key": "value"})
response = input_client.create_input_by_prompt(
    text="Saurav28286 what is {{x}} and {{y}}",
    context="This is {{c}}",
    input_data=input_data,
    template_name="temp3113"
)
print("Create input by prompt:", response.dict())

# Example: Create input using OpenAI messages
openai_messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the weather like today?"},
    {"role": "assistant", "content": "The weather is sunny with a high of 25°C."}
]
response = input_client.create_input_by_openai(
    messages=openai_messages,
    template_name="OpenAI 1186 Template",
    expected_output="Sunny weather forecast",
    metadata={"source": "OpenAI"}
)
print("Create input by OpenAI:", response.dict())
```

## CandidateModel

The `CandidateModel` class is used for managing candidate models. You can create, update, and manage candidate models with this class.

### CandidateModel Methods

- **create_candidate_model**  
  Creates a candidate model.

- **update_candidate_model**  
  Updates an existing candidate model.

- **get_candidate_model_by_id**  
  Retrieves a candidate model by its ID.

- **delete_candidate_model**  
  Deletes a candidate model by its ID.

### CandidateModel Examples

```python
from evaluableai.client import EvaluableAI
from evaluableai.objects.candidate_model import CandidateModel

client = EvaluableAI()
candidate_model_client = CandidateModel(client=client)

# Example: Create candidate model
model_data = {
    "name": "Test Model",
    "version": "1.0.0",
    "description": "A test candidate model"
}
response = candidate_model_client.create_candidate_model(model_data)
print("Create candidate model:", response.dict())

# Example: Update candidate model
model_id = "candidate-12345"
update_data = {
    "description": "Updated description for the model"
}
response = candidate_model_client.update_candidate_model(model_id, update_data)
print("Update candidate model:", response.dict())

# Example: Get candidate model by ID
response = candidate_model_client.get_candidate_model_by_id(model_id)
print("Get candidate model by ID:", response.dict())

# Example: Delete candidate model
response = candidate_model_client.delete_candidate_model(model_id)
print("Delete candidate model:", response.dict())
```

## Response

The `Response` class is used for managing and evaluating responses from models. It supports creating responses, updating them, and more.

### Response Methods

- **create_response**  
  Creates a response object.

- **update_response**  
  Updates an existing response.

- **get_response_by_id**  
  Retrieves a response by its ID.

- **delete_response**  
  Deletes a response by its ID.

### Response Examples

```python
from evaluableai.client import EvaluableAI
from evaluableai.objects.response import Response

client = EvaluableAI()
response_client = Response(client=client)

# Example: Create response
response_data = {
    "model_id": "model-12345",
    "input_id": "input-54321",
    "output": "This is the model output"
}
response = response_client.create_response(response_data)
print("Create response:", response.dict())

# Example: Update response
response_id = "response-67890"
update_data = {
    "output": "Updated model output"
}
response = response_client.update_response(response_id, update_data)
print("Update response:", response.dict())

# Example: Get response by ID
response = response_client.get_response_by_id(response_id)
print("Get response by ID:", response.dict())

# Example: Delete response
response = response_client.delete_response(response_id)
print("Delete response:", response.dict())
```

## Evaluable AI Python SDK - Tag Management

The Evaluable AI SDK includes comprehensive functionality for managing tags. This includes creating, updating, deleting, and associating tags with responses and inputs.

### Documentation

For detailed documentation, please refer to [Evaluable AI Docs](https://docs.evaluable.ai/).

### Setup

1. **Register** using this [link](https://portal.evaluable.ai/signin).
2. **Navigate to the settings page**.
3. **Under the section Evaluable AI keys**, provide a key name and click generate. Securely save the API key. The key can only be copied at the time of creation.
4. **Optional**: Add your key to an environment variable `EVALUABLEAI_API_KEY`.
5. **Install the SDK**:
    ```bash
    pip install -e /path/to/evaluableai_package
    ```

### Tag Management

The `Tag` class provides methods to manage tags in the Evaluable AI platform.

#### Initialization

To use the tag management functionalities, you need to initialize the `Tag` class with an `EvaluableAI` client:

```python
from evaluableai.client import EvaluableAI
from tag import Tag

token = os.getenv("EVALUABLEAI_API_KEY")
client = EvaluableAI(token=token)
tag_manager = Tag(client)
```

#### Tag Management Methods

- **Create a Tag**  
  Create a new tag by providing a tag name and optionally a color:

  ```python
  response = tag_manager.create_tag(tag_name="NewTag", color="#FF5733")
  print("Create Tag Response:", response)
  ```

- **Create Tags in Bulk**  
  To create multiple tags at once, provide a list of tags:

  ```python
  tags = [
      {"tag_name": "Tag1", "color": "#FF5733"},
      {"tag_name": "Tag2", "color": "#33FF57"}
  ]
  response = tag_manager.create_tags_bulk(tags)
  print("Create Tags in Bulk Response:", response)
  ```

- **Update a Tag**  
  Update an existing tag by providing the tag ID and the fields to update:

  ```python
  response = tag_manager.update_tag(tag_id="tag-id", tag_name="UpdatedTag", color="#3357FF")
  print("Update Tag Response:", response)
  ```

- **Get Tag by Name**  
  Retrieve a tag's details by its name:

  ```python
  response = tag_manager.get_tag_by_name(tag_name="ExistingTag")
  print("Get Tag by Name Response:", response)
  ```

- **Delete Tag by Name**  
  Delete a tag by its name:

  ```python
  response = tag_manager.delete_tag_by_name(tag_name="TagToDelete")
  print("Delete Tag by Name Response:", response)
  ```

- **Add Tags to Responses**  
  Add tags to multiple responses:

  ```python
  response = tag_manager.add_tags_to_responses(tag_names=["Tag1", "Tag2"], response_ids=["response-id1", "response-id2"])
  print("Add Tags to Responses Response:", response)
  ```

- **Remove Tags from Responses**  
  Remove tags from multiple responses:

  ```python
  response = tag_manager.remove_tags_from_responses(tag_names=["Tag1", "Tag2"], response_ids=["response-id1", "response-id2"])
  print("Remove Tags from Responses Response:", response)
  ```

- **Add Tags to

 Inputs**  
  Add tags to multiple inputs:

  ```python
  response = tag_manager.add_tags_to_inputs(tag_names=["Tag1", "Tag2"], input_ids=["input-id1", "input-id2"])
  print("Add Tags to Inputs Response:", response)
  ```

- **Remove Tags from Inputs**  
  Remove tags from multiple inputs:

  ```python
  response = tag_manager.remove_tags_from_inputs(tag_names=["Tag1", "Tag2"], input_ids=["input-id1", "input-id2"])
  print("Remove Tags from Inputs Response:", response)
  ```

- **Get Tags by Type**  
  Retrieve tags by their type:

  ```python
  response = tag_manager.get_tags_by_type(tag_type="response")
  print("Get Tags by Type Response:", response)
  ```

- **Get Tag Associations**  
  Retrieve all associations of a specific tag:

  ```python
  response = tag_manager.get_tag_associations(tag_id="tag-id")
  print("Get Tag Associations Response:", response)
  ```

### Parameters for Evaluation

All the parameters required for evaluating responses and for seeing the evaluation runs on the UI are passed in the `evaluableai_params`. Below is a list of all parameters:

- **token**: Your Evaluable AI API Key.
- **tag_names**: Tags for categorizing the evaluation.
- **model_name**: The name of the model being used.

## Requirements

- Python 3.9 or higher.
```

This `README.md` now includes the sections for `Input`, `CandidateModel`, `Response`, and `Tag Management`, and is formatted for easy use in a project.