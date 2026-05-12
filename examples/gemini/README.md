### Evaluable AI Python SDK

The SDK facilitates seamless integration between performing inferences using various AI models and evaluating those responses on the Evaluable AI platform.

#### Documentation

For detailed documentation, please refer to [Evaluable AI Docs](https://evaluable.ai/docs).

### Gemini Integration

The Gemini integration allows you to use Google's Generative AI models with Evaluable AI. This integration includes both synchronous and asynchronous capabilities for generating content and evaluating responses.

#### Setup

1. **Register** using this [link](https://evaluable.ai/register).
2. **Navigate to the settings page**.
3. **Under the section Evaluable AI keys**, provide a key name and click generate. Securely save the API key. The key can only be copied at the time of creation.
4. **Optional**: Add your key to an environment variable `EVALUABLEAI_API_KEY`.
5. **Install the SDK**:
    ```bash
    pip install -e /path/to/evaluableai_package
    ```

#### Usage

In your code, you will need to initialize the `CustomGenerativeModel` with the appropriate parameters. You can optionally provide an `API_KEY` directly or use the environment variable `GOOGLE_API_KEY`.

#### Example Script for Synchronous Execution

Create a script, `demo.py`, for synchronous execution:

```python
#!/usr/bin/env -S poetry run python
from evaluableai import GeminiAI

# Initialize the custom model
custom_model = GeminiAI(
    API_KEY="Your_Google_API_Key",  # Optional, if not provided, it will use the environment variable
    evaluableai_params={
        "token": "Your_EvaluableAI_API_Key",
        "eval": False,
        "sampling": 1,
        "eval_list": ["Sentiment"],
        "async": False,
        "tag_names": ["EXP 1", "GEMINI AI"],
        "model_name": "gemini-1.0-pro"
    }
)

# Data Generation
fact_questions_with_answers = [
    ["What is the only mammal capable of true flight?", "Bats"],
    ["In what year did Neil Armstrong and Buzz Aldrin land on the moon?", "1969"],
    ["What is the hardest natural substance on Earth?", "Diamond"],
    ["Which planet is known as the Red Planet?", "Mars"],
    ["What is the largest ocean on Earth?", "Pacific Ocean"],
    ["How long does it take for light from the Sun to reach Earth?", "About 8 minutes"],
    ["What is the chemical symbol for table salt?", "NaCl"],
    ["Which animal has the highest blood pressure?", "Giraffe"],
    ["What temperature does water boil at under normal conditions?", "100 degrees Celsius"],
    ["Which is the largest planet in our solar system?", "Jupiter"]
]

def main():
    for question, ground_truth in fact_questions_with_answers:
        response = custom_model.generate_content(
            contents=[{
                "role": "user",
                "parts": [{"text": question}]
            }],
            ground_truth=ground_truth,
            tools=None,
            tool_config=None,
            safety_settings=None,
            generation_config=None
        )
        result = response.candidates[0].content.parts[0].text
        print(f"Question: {question} -> Answer: {result} (Expected: {ground_truth})")

if __name__ == "__main__":
    main()
```

#### Example Script for Asynchronous Execution

Create a script, `demo_async.py`, for asynchronous execution:

```python
import os
import asyncio
from evaluableai import GeminiAI

# Initialize the custom model
custom_model = GeminiAI(
    API_KEY="Your_Google_API_Key",  # Optional, if not provided, it will use the environment variable
    evaluableai_params={
        "token": "Your_EvaluableAI_API_Key",
        "eval": False,
        "sampling": 1,
        "eval_list": ["Sentiment"],
        "async": True,
        "tag_names": ["EXP 1", "GEMINI AI"],
        "model_name": "gemini-1.0-pro"
    }
)

# Data Generation
fact_questions_with_answers = [
    ["What is the only mammal capable of true flight?", "Bats"],
    ["In what year did Neil Armstrong and Buzz Aldrin land on the moon?", "1969"],
    ["What is the hardest natural substance on Earth?", "Diamond"],
    ["Which planet is known as the Red Planet?", "Mars"],
    ["What is the largest ocean on Earth?", "Pacific Ocean"],
    ["How long does it take for light from the Sun to reach Earth?", "About 8 minutes"],
    ["What is the chemical symbol for table salt?", "NaCl"],
    ["Which animal has the highest blood pressure?", "Giraffe"],
    ["What temperature does water boil at under normal conditions?", "100 degrees Celsius"],
    ["Which is the largest planet in our solar system?", "Jupiter"]
]

async def main():
    for question, ground_truth in fact_questions_with_answers:
        response = await custom_model.generate_content_async(
            contents=[{
                "role": "user",
                "parts": [{"text": question}]
            }],
            ground_truth=ground_truth,
            tools=None,
            tool_config=None,
            safety_settings=None,
            generation_config=None
        )
        print(f"Question: {question} -> Answer: {response.candidates[0].content.parts[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
```

In these examples, replace `Your_Google_API_Key` and `Your_EvaluableAI_API_Key` with your actual API keys. This setup ensures that you can use the Gemini models in both synchronous and asynchronous modes while leveraging the Evaluable AI platform for evaluation and analysis.

### Parameters for Evaluation

All the parameters required for evaluating responses and for seeing the evaluation runs on the UI are passed in the `evaluableai_params`. Below is a list of all parameters:

- `token`: Your Evaluable AI API Key.
- `eval`: Boolean to specify if evaluation should be performed.
- `sampling`: Sampling rate for evaluation.
- `eval_list`: List of evaluation metrics to use.
- `async`: Boolean to specify if the request should be asynchronous.
- `tag_names`: Tags for categorizing the evaluation.
- `model_name`: The name of the model being used.


Input Management
The SDK provides functionality to manage inputs using templates or prompts.

Create Input by Template ID
import os
from evaluableai import EvaluableAI

token = os.getenv("EVALUABLEAI_API_KEY")
client = EvaluableAI(token=token)

template_id = "template-id"
input_data = {
    "variables": {"company": "value1"},
    "expected_output": "",
    "metadata": {"key": "value"}
}

response = client.create_input_by_template_id(template_id, input_data, token, client)
print("Create input by template ID:", response.dict())


Create Multiple Inputs by Template ID
inputs = [
    {
        "variables": {"x": "LLM", "y": "Llama", "c": "abc"},
        "expected_output": "",
        "metadata": {"key": "value"}
    },
    {
        "variables": {"x": "Night", "y": "moon", "c": "def"},
        "expected_output": "",
        "metadata": {"key": "value"}
    },
    {
        "variables": {"x": "Day", "y": "sun", "c": "ghi"},
        "expected_output": "",
        "metadata": {"key": "value"}
    }
]

response = client.create_many_input_by_template_id(template_id, inputs, token, client)
print("Create multiple inputs by template ID:", response.dict())

Create Input by Prompt

text = "Example prompt"
context = "Example context"
input_data = {
    "variables": {"company": "value1"},
    "expected_output": "",
    "metadata": {"key": "value"}
}

response = client.create_input_by_prompt(text, context, input_data, client, token, "Example2 Template2")
print("Create input by prompt:", response.dict())

Create Multiple Inputs by Prompt
text = "Define what is {{x}} and {{y}}"
context = "This is {{c}}"
inputs = [
    {
        "variables": {"x": "LLM", "y": "Llama", "c": "abc"},
        "expected_output": "",
        "metadata": {"key": "value"}
    },
    {
        "variables": {"x": "Night", "y": "moon", "c": "def"},
        "expected_output": "",
        "metadata": {"key": "value"}
    },
    {
        "variables": {"x": "Day", "y": "sun", "c": "ghi"},
        "expected_output": "",
        "metadata": {"key": "value"}
    }
]

response = client.create_many_inputs_by_prompt(text, context, inputs, client, token, "Example Template2")
print("Create multiple inputs by prompt:", response.dict())

Create Input using OpenAI Standard

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "system", "content": "In the country {{a}}"},
    {"role": "user", "content": "who is the md of {{x}}"}
]

response = client.create_input_by_openai(messages, token, client, "Example OpenAI Template")
print("Create input by OpenAI:", response.dict())


Requirements
Python 3.9 or higher.

For more information, visit the [Evaluable AI Docs](https://evaluable.ai/docs).