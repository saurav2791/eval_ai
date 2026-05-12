import os
import random
import logging
from evaluableai.client import EvaluableAI, AsyncEvaluableAI
from evaluableai.exceptions import EvaluableAIError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_evaluableai_client(api_key, token):
    try:
        os.environ["GOOGLE_API_KEY"] = api_key
        eval_client = EvaluableAI(token=token)
        return eval_client
    except Exception as e:
        logger.error(f"Failed to initialize EvaluableAI client: {str(e)}")
        raise EvaluableAIError(f"Initialization failed: {str(e)}")

def initialize_async_evaluableai_client(api_key, token):
    try:
        os.environ["GOOGLE_API_KEY"] = api_key
        eval_client = AsyncEvaluableAI(token=token)
        return eval_client
    except Exception as e:
        logger.error(f"Failed to initialize AsyncEvaluableAI client: {str(e)}")
        raise EvaluableAIError(f"Initialization failed: {str(e)}")

def is_selected_for_eval(probability):
    selected = random.random() <= probability
    logger.info(f"Selected for eval: {selected} with probability {probability}")
    return selected

def generation_config_to_dict(generation_config):
    try:
        return {
            "max_output_tokens": generation_config.max_output_tokens,
            "temperature": generation_config.temperature,
            "top_p": generation_config.top_p,
            "top_k": generation_config.top_k,
            "candidate_count": generation_config.candidate_count,
            "stop_sequences": list(generation_config.stop_sequences),
            "response_mime_type": generation_config.response_mime_type,
        }
    except AttributeError as e:
        logger.error(f"Error converting generation config to dict: {str(e)}")
        raise EvaluableAIError(f"Conversion error: {str(e)}")

def function_call_to_dict(function_call):
    try:
        return {
            "name": function_call.name,
            "arguments": function_call.arguments,
        }
    except AttributeError as e:
        logger.error(f"Error converting function call to dict: {str(e)}")
        raise EvaluableAIError(f"Conversion error: {str(e)}")

def content_to_dict(content):
    try:
        return {
            "role": getattr(content, "role", None),
            "parts": [part_to_dict(part) for part in content.parts],
        }
    except AttributeError as e:
        logger.error(f"Error converting content to dict: {str(e)}")
        raise EvaluableAIError(f"Conversion error: {str(e)}")

def part_to_dict(part):
    try:
        return {
            "text": part.text,
            "function_call": function_call_to_dict(part.function_call) if part.function_call else None,
        }
    except AttributeError as e:
        logger.error(f"Error converting part to dict: {str(e)}")
        raise EvaluableAIError(f"Conversion error: {str(e)}")

def generate_content_request_to_dict(request):
    try:
        return {
            "model": request.model,
            "contents": [content_to_dict(content) for content in request.contents],
            "generation_config": generation_config_to_dict(request.generation_config),
            "safety_settings": [],
            "tools": [],
            "tool_config": None,
            "system_instruction": None,
            "cached_content": "",
        }
    except AttributeError as e:
        logger.error(f"Error converting generate content request to dict: {str(e)}")
        raise EvaluableAIError(f"Conversion error: {str(e)}")

def safety_rating_to_dict(safety_rating):
    try:
        return {
            "category": safety_rating.category,
            "probability": safety_rating.probability,
        }
    except AttributeError as e:
        logger.error(f"Error converting safety rating to dict: {str(e)}")
        raise EvaluableAIError(f"Conversion error: {str(e)}")

def candidate_to_dict(candidate):
    try:
        return {
            "content": content_to_dict(candidate.content),
            "finish_reason": candidate.finish_reason,
            "index": candidate.index,
            "safety_ratings": [safety_rating_to_dict(rating) for rating in candidate.safety_ratings],
        }
    except AttributeError as e:
        logger.error(f"Error converting candidate to dict: {str(e)}")
        raise EvaluableAIError(f"Conversion error: {str(e)}")

def prompt_feedback_to_dict(prompt_feedback):
    try:
        return {
            "rating": getattr(prompt_feedback, "rating", None),
            "feedback_text": getattr(prompt_feedback, "feedback_text", None),
        }
    except AttributeError as e:
        logger.error(f"Error converting prompt feedback to dict: {str(e)}")
        raise EvaluableAIError(f"Conversion error: {str(e)}")

def usage_metadata_to_dict(usage_metadata):
    try:
        return {
            "prompt_token_count": usage_metadata.prompt_token_count,
            "candidates_token_count": usage_metadata.candidates_token_count,
            "total_token_count": usage_metadata.total_token_count,
        }
    except AttributeError as e:
        logger.error(f"Error converting usage metadata to dict: {str(e)}")
        raise EvaluableAIError(f"Conversion error: {str(e)}")

def generate_content_response_to_dict(response):
    try:
        return {
            "candidates": [candidate_to_dict(candidate) for candidate in response.candidates],
            "prompt_feedback": prompt_feedback_to_dict(response.prompt_feedback),
            "usage_metadata": usage_metadata_to_dict(response.usage_metadata),
        }
    except AttributeError as e:
        logger.error(f"Error converting generate content response to dict: {str(e)}")
        raise EvaluableAIError(f"Conversion error: {str(e)}")
