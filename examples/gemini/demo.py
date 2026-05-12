#!/usr/bin/env -S poetry run python
import os
import logging
from evaluableai import GeminiAI
from evaluableai.exceptions import EvaluableAIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the custom model
custom_model = GeminiAI(
    evaluableai_params={
        "token": os.getenv("EVALUABLEAI_API_KEY"),
        "eval": False,
        "sampling": 1,
        "eval_list": ["Sentiment"],
        "model_name": "gemini-1.0-pro"
    }
)

# Data Generation
fact_questions_with_answers = [
    ["What is the only mammal capable of true flight?", "Bats"],
]

def generate_and_log_response(question, ground_truth):
    try:
        response = custom_model.generate_content(
            [{
                "role": "user",
                "parts": [{
                    "text": question
                }]
            }],
            ground_truth=ground_truth,
            tools=None,
            tool_config=None,
            safety_settings=None,
            generation_config=None
        )
        result = response.candidates[0].content.parts[0].text
        logger.info(f"Question: {question} -> Answer: {result} (Expected: {ground_truth})")
    except EvaluableAIError as e:
        logger.error(f"Failed to generate content for question: {question}. Error: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")

def main():
    for question, ground_truth in fact_questions_with_answers:
        generate_and_log_response(question, ground_truth)

if __name__ == "__main__":
    main()
