# LLMScorer

The `LLMScorer` class is a part of the EvaluableAI SDK and is used to interact with LLM Scorers in the EvaluableAI system. It allows you to create, retrieve, and delete LLM Scorers using YAML configuration files or direct method calls.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Initialization](#initialization)
  - [Creating an LLM Scorer](#creating-an-llm-scorer)
  - [Retrieving LLM Scorers](#retrieving-llm-scorers)
  - [Deleting an LLM Scorer](#deleting-an-llm-scorer)
- [YAML Configuration](#yaml-configuration)
- [Example](#example)
- [Running Tests](#running-tests)

## Installation

To use the `LLMScorer` class, ensure you have the EvaluableAI SDK installed in your environment. You can install it using pip:

```bash
pip install evaluableai
```

## Usage

### Initialization

To begin using the `LLMScorer`, you need to initialize it with a valid `EvaluableAI` client instance:

```python
from evaluableai.client import EvaluableAI
from evaluableai.Scorer.llm_scorer import LLMScorer

client = EvaluableAI(token="your_api_token")
llm_scorer = LLMScorer(client=client)
```

### Creating an LLM Scorer

You can create an LLM Scorer either by loading a YAML configuration file or by directly passing a dictionary with the required fields.

#### From YAML File

```python
scorer_data = llm_scorer.create_scorer_from_yaml('path/to/your/llm_scorer.yaml')
```

#### Directly from a Dictionary

```python
scorer_data = {
    "scorer_name": "test_scorer",
    "scorer_type": "user",
    "scorer_prompt": "Evaluate sentiment...",
    "output_format_type": "Choices",
    "score_description": "Test scorer",
    "scorer_variables": [{"name": "llm_output", "required": True}],
    "output_categories": [
        {"name": "A", "color": "green", "value": "100"},
        {"name": "B", "color": "yellow", "value": "50"}
    ],
    "eval_model": {"model_name": "OPENAI", "model_version": "gpt-4"}
}

response = llm_scorer.create_scorer(scorer_data)
```

### Retrieving LLM Scorers

You can retrieve a list of all LLM Scorers, or retrieve specific ones by their ID or name.

#### Get All Scorers

```python
scorers = llm_scorer.get_scorers()
```

#### Get Scorer by ID

```python
scorer = llm_scorer.get_scorer_by_id('scorer_id')
```

#### Get Scorer by Name

```python
scorer = llm_scorer.get_scorer_by_name('scorer_name')
```

### Deleting an LLM Scorer

To delete an LLM Scorer, you can use the `delete_scorer` method:

```python
delete_response = llm_scorer.delete_scorer('scorer_id')
```

## YAML Configuration

The `LLMScorer` class uses YAML files to configure the creation of new LLM Scorers. Below is an example of what the YAML file might look like:

```yaml
scorer_name: "test_scorer"
scorer_type: "user"
scorer_prompt: "Evaluate sentiment..."
output_format_type: "Choices"
score_description: "Test scorer"
scorer_variables:
  - name: "llm_output"
    required: True
output_categories:
  - name: "A"
    color: "green"
    value: "100"
  - name: "B"
    color: "yellow"
    value: "50"
eval_model:
  model_name: "OPENAI"
  model_version: "gpt-4"
```

## Example

Here’s a simple example demonstrating how to use the `LLMScorer` class:

```python
from evaluableai.client import EvaluableAI
from evaluableai.Scorer.llm_scorer import LLMScorer

client = EvaluableAI(token="your_api_token")
llm_scorer = LLMScorer(client=client)

# Create scorer from YAML
response = llm_scorer.create_scorer_from_yaml('path/to/your/llm_scorer.yaml')
print(response)

# Retrieve all scorers
scorers = llm_scorer.get_scorers()
print(scorers)

# Get scorer by ID
scorer = llm_scorer.get_scorer_by_id(response['scorer_id'])
print(scorer)

# Delete scorer
delete_response = llm_scorer.delete_scorer(response['scorer_id'])
print(delete_response)
```

## Running Tests

Unit tests for the `LLMScorer` class can be run using the following command:

```bash
python -m unittest discover -s tests -p '*_test.py'
```

Ensure your tests cover various scenarios, including creation, retrieval, and deletion of LLM Scorers.

---

# HeuristicScorer

The `HeuristicScorer` class is also part of the EvaluableAI SDK and is used to interact with heuristic scorers within the system. Similar to the `LLMScorer`, it allows you to create, update, retrieve, and delete heuristic scorers using YAML configuration files or direct method calls.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Initialization](#initialization)
  - [Creating a Heuristic Scorer](#creating-a-heuristic-scorer)
  - [Updating a Heuristic Scorer](#updating-a-heuristic-scorer)
  - [Retrieving Heuristic Scorers](#retrieving-heuristic-scorers)
  - [Deleting a Heuristic Scorer](#deleting-a-heuristic-scorer)
- [YAML Configuration](#yaml-configuration)
- [Example](#example)
- [Running Tests](#running-tests)

## Installation

To use the `HeuristicScorer` class, ensure you have the EvaluableAI SDK installed in your environment. You can install it using pip:

```bash
pip install evaluableai
```

## Usage

### Initialization

To begin using the `HeuristicScorer`, you need to initialize it with a valid `EvaluableAI` client instance:

```python
from evaluableai.client import EvaluableAI
from evaluableai.Scorer.heuristic_scorer import HeuristicScorer

client = EvaluableAI(token="your_api_token")
heuristic_scorer = HeuristicScorer(client=client)
```

### Creating a Heuristic Scorer

You can create a Heuristic Scorer either by loading a YAML configuration file or by directly passing a dictionary with the required fields.

#### From YAML File

```python
scorer_data = heuristic_scorer.create_scorer_from_yaml('path/to/your/heuristic_scorer.yaml')
```

#### Directly from a Dictionary

```python
scorer_data = {
    "scorer_name": "meteor",
    "scorer_type": "user",
    "scorer_display_name": "METEOR",
    "scorer_function": "Pseudo code...",
    "score_type": "Double",
    "scorer_short_description": "Evaluates translation quality...",
    "scorer_long_description": "The METEOR scorer...",
    "scorer_variables": [
        {
            "name": "referenceTexts",
            "type": "List<String>",
            "source": "ground_truth",
            "description": "A list of reference translations."
        },
        {
            "name": "translatedText",
            "type": "String",
            "source": "llm_output",
            "description": "The machine-translated text to evaluate."
        }
    ]
}

response = heuristic_scorer.create_scorer(scorer_data)
```

### Updating a Heuristic Scorer

You can update an existing Heuristic Scorer by its ID:

```python
updated_data = {
    # Your updated data here
}

update_response = heuristic_scorer.update_scorer('scorer_id', updated_data)
```

### Retrieving Heuristic Scorers

You can retrieve a list of all Heuristic Scorers, or retrieve specific ones by their ID or name.

#### Get All Scorers

```python
scorers = heuristic_scorer.get_scorers()
```

#### Get Scorer by ID

```python
scorer = heuristic_scorer.get_scorer_by_id('scorer_id')
```

#### Get Scorer by Name

```python
scorer = heuristic_scorer.get_scorer_by_name('scorer_name')
```

### Deleting a Heuristic Scorer

To delete a Heuristic Scorer, you can use the `delete_scorer` method:

```python
delete_response = heuristic_scorer.delete_scorer('scorer_id')
```

## YAML Configuration

The `HeuristicScorer` class uses YAML files to configure the creation of new He

uristic Scorers. Below is an example of what the YAML file might look like:

```yaml
scorer_name: "meteor"
scorer_type: "user"
scorer_display_name: "METEOR"
scorer_function: "Pseudo code..."
score_type: "Double"
scorer_short_description: "Evaluates translation quality..."
scorer_long_description: "The METEOR scorer..."
scorer_variables:
  - name: "referenceTexts"
    type: "List<String>"
    source: "ground_truth"
    description: "A list of reference translations."
  - name: "translatedText"
    type: "String"
    source: "llm_output"
    description: "The machine-translated text to evaluate."
```

## Example

Here’s a simple example demonstrating how to use the `HeuristicScorer` class:

```python
from evaluableai.client import EvaluableAI
from evaluableai.Scorer.heuristic_scorer import HeuristicScorer

client = EvaluableAI(token="your_api_token")
heuristic_scorer = HeuristicScorer(client=client)

# Create scorer from YAML
response = heuristic_scorer.create_scorer_from_yaml('path/to/your/heuristic_scorer.yaml')
print(response)

# Retrieve all scorers
scorers = heuristic_scorer.get_scorers()
print(scorers)

# Get scorer by ID
scorer = heuristic_scorer.get_scorer_by_id(response['scorer_id'])
print(scorer)

# Update scorer
updated_data = {
    # Your updated data here
}
update_response = heuristic_scorer.update_scorer(response['scorer_id'], updated_data)
print(update_response)

# Delete scorer
delete_response = heuristic_scorer.delete_scorer(response['scorer_id'])
print(delete_response)
```

## Running Tests

Unit tests for the `HeuristicScorer` class can be run using the following command:

```bash
python -m unittest discover -s tests -p '*_test.py'
```

Ensure your tests cover various scenarios, including creation, updating, retrieval, and deletion of Heuristic Scorers.



