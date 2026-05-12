import os
import asyncio
import logging
from evaluableai import GeminiAI
from evaluableai.exceptions import EvaluableAIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up environment variables
os.environ["GOOGLE_API_KEY"] = "AIzaSyDkh79oMK18XFXWZTDTl2-kTrJtyqw0CdI"

evaluableai_params = {
    "token": os.getenv("EVALUABLEAI_API_KEY"),
    "eval": False,
    "sampling": 1,
    "eval_list": ["Sentiment"],
    "async": True,
    "tag_names": ["EXP 3", "Gemini AI"],
    "model_name": "gemini-1.0-pro-latest"
}

# Initialize the custom model
custom_model = GeminiAI(
    evaluableai_params=evaluableai_params
)

fact_questions_with_answers = [
    ["Which is the largest planet in our solar system?", "Jupiter"]
]

async def generate_and_log_response(message, ground_truth):
    try:
        response = await custom_model.generate_content_async(
            contents=[{"role": "user", "parts": [{"text": message}]}],
            ground_truth=ground_truth,
            tools=None,
            tool_config=None,
            safety_settings=None,
            generation_config=None
        )
        result = response.candidates[0].content.parts[0].text
        logger.info(f"Message: {message} -> Result: {result} (Expected: {ground_truth})")
    except EvaluableAIError as e:
        logger.error(f"Failed to generate content for message: {message}. Error: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")

async def main():
    tasks = [
        generate_and_log_response(message, ground_truth)
        for message, ground_truth in fact_questions_with_answers
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
    logger.info("Process completed.")
