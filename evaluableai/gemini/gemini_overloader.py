import os
import json
import time
import google.generativeai as genai
from evaluableai.exceptions import EvaluableAIError
import asyncio
from typing import Union, Any
import threading
import logging
from evaluableai.gemini.helper import (
    initialize_evaluableai_client,
    initialize_async_evaluableai_client,
    generate_content_request_to_dict,
    generate_content_response_to_dict,
    is_selected_for_eval,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to load the endpoint configuration from the endpoint.json file
def load_config() -> dict:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(current_dir, '..', 'endpoint.json')
    config_file = os.path.normpath(config_file)

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found at: {config_file}")

    with open(config_file, 'r') as f:
        return json.load(f)

# Load the configuration once for global usage
config = load_config()

class CustomGenerativeModel(genai.GenerativeModel):
    def __init__(self, evaluableai_params, *args, **kwargs):
        api_key = kwargs.pop("API_KEY", None) or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "API_KEY must be provided either directly or through the environment variable 'GOOGLE_API_KEY'."
            )

        self.eval_client = initialize_evaluableai_client(api_key, evaluableai_params["token"])
        self.async_eval_client = initialize_async_evaluableai_client(api_key, evaluableai_params["token"])
        self.evaluableai_params = evaluableai_params
        genai.configure(api_key=api_key)
        super().__init__(evaluableai_params["model_name"], *args, **kwargs)

    def generate_content(self, contents, *args, **kwargs):
        ground_truth = kwargs.pop('ground_truth', None)
        stream = kwargs.pop('stream', False)
        logger.info("Custom generate_content called")
        request = self._prepare_request(
            contents=contents,
            generation_config=kwargs.get('generation_config'),
            safety_settings=kwargs.get('safety_settings'),
            tools=kwargs.get('tools'),
            tool_config=kwargs.get('tool_config')
        )

        request_data = generate_content_request_to_dict(request)

        local_evaluableai_params = self.evaluableai_params.copy()
        local_evaluableai_params["ground_truth"] = ground_truth  # Add ground truth information
        try:
            start_time = time.time()
            if stream:
                response = super().stream_generate_content(contents, **kwargs)
            else:
                response = super().generate_content(contents, *args, **kwargs)
            end_time = time.time()
            duration_in_ms = (end_time - start_time) * 1000
            local_evaluableai_params["time_taken"] = round(duration_in_ms, 3)
        except Exception as e:
            logger.error(f"Error during generate_content: {str(e)}")
            raise

        if stream:
            return response

        response_data = generate_content_response_to_dict(response)

        skip_submit = local_evaluableai_params.pop("skip_submit", None)
        if skip_submit:
            return response

        if "async" in local_evaluableai_params and local_evaluableai_params["async"]:
            def run_async_post():
                asyncio.run(
                    self.post_to_server_async(request_data, response_data, local_evaluableai_params))

            thread = threading.Thread(target=run_async_post)
            thread.start()
        else:
            self.post_to_server(request_data, response_data, local_evaluableai_params)

        return response

    async def generate_content_async(self, contents, *args, **kwargs):
        ground_truth = kwargs.pop('ground_truth', None)
        stream = kwargs.pop('stream', False)
        request = self._prepare_request(
            contents=contents,
            generation_config=kwargs.get('generation_config'),
            safety_settings=kwargs.get('safety_settings'),
            tools=kwargs.get('tools'),
            tool_config=kwargs.get('tool_config')
        )

        request_data = generate_content_request_to_dict(request)

        local_evaluableai_params = self.evaluableai_params.copy()
        local_evaluableai_params["ground_truth"] = ground_truth  # Add ground truth information
        try:
            start_time = time.time()
            if stream:
                response = super().stream_generate_content(contents, **kwargs)
            else:
                response = await super().generate_content_async(contents, *args, **kwargs)
            end_time = time.time()
            duration_in_ms = (end_time - start_time) * 1000
            local_evaluableai_params["time_taken"] = round(duration_in_ms, 3)
        except Exception as e:
            logger.error(f"Error during generate_content_async: {str(e)}")
            raise

        if stream:
            return response

        response_data = generate_content_response_to_dict(response)

        skip_submit = local_evaluableai_params.pop("skip_submit", None)
        if skip_submit:
            return response

        if "async" in local_evaluableai_params and local_evaluableai_params["async"]:
            await self.post_to_server_async(request_data, response_data, local_evaluableai_params)
        else:
            self.post_to_server(request_data, response_data, local_evaluableai_params)

        return response

    def post_to_server(self, request_data, response_data, evaluableai_params):
        try:
            sampling_rate = evaluableai_params.pop("sampling", None)
            sampling_flag = True
            if sampling_rate is not None:
                sampling_flag = is_selected_for_eval(sampling_rate)
                evaluableai_params["sampling_flag"] = sampling_flag

            endpoint = config['gemini_submit_data']
            if "eval" in evaluableai_params and evaluableai_params["eval"] and sampling_flag:
                endpoint = config['gemini_submit_data_and_eval']

            body = {
                "gemini_request": request_data,
                "gemini_response": response_data,
                "evaluableai_params": evaluableai_params
            }

            response = self.eval_client.make_request(method="POST", endpoint=endpoint, data=body)
            if response is None:
                raise EvaluableAIError("No response received from the evaluation server.")

            if response.status_code not in [200, 201]:
                raise EvaluableAIError(
                    f"Failed to post data to evaluable ai server: {response.status_code}, {response.text}")
        except Exception as e:
            logger.error(f"Failed to post data to evaluable ai server: {str(e)}")
            raise

    async def post_to_server_async(self, request_data, response_data, evaluableai_params):
        try:
            sampling_rate = evaluableai_params.pop("sampling", None)
            sampling_flag = True
            if sampling_rate is not None:
                sampling_flag = is_selected_for_eval(sampling_rate)
                evaluableai_params["sampling_flag"] = sampling_flag

            endpoint = config['gemini_submit_data']
            if "eval" in evaluableai_params and evaluableai_params["eval"] and sampling_flag:
                endpoint = config['gemini_submit_data_and_eval']

            body = {
                "gemini_request": request_data,
                "gemini_response": response_data,
                "evaluableai_params": evaluableai_params
            }

            response = await self.async_eval_client.async_make_request(method="POST", endpoint=endpoint, data=body)

            if response is None:
                raise EvaluableAIError("No response received from the evaluation server.")

            if response.status_code not in [200, 201]:
                raise EvaluableAIError(
                    f"Failed to post data to evaluable ai server: {response.status_code}, {response.text}")
        except Exception as e:
            logger.error(f"Failed to post data to evaluable ai server: {str(e)}")
            raise
