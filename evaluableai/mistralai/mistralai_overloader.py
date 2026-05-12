import os
import time
import random
import asyncio
import threading
from typing import Dict, Any
from pydantic import BaseModel
from mistralai.client import MistralClient as BaseMistralClient
from mistralai.models.chat_completion import ChatCompletionResponse
from mistralai.exceptions import MistralException
from evaluableai.client import EvaluableAI
from evaluableai.exceptions import EvaluableAIError
from evaluableai.util import validate_evaluableai_params
import logging
import json

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


def is_selected_for_eval(probability):
    """Random selection based on the given probability."""
    rand_num = random.random()
    return rand_num <= probability  # True if selected, False if not


class MistralClientOverloader(BaseMistralClient):
    eval_client: EvaluableAI

    def __init__(self, api_key: str, evaluableai_params: Dict[str, Any] = None, **kwargs) -> None:
        super().__init__(api_key=api_key, **kwargs)
        if evaluableai_params is None:
            evaluableai_params = {}
        token = evaluableai_params.pop("token", None)
        validate_evaluableai_params(evaluableai_params)
        self.evaluableai_params = evaluableai_params
        self.eval_client = EvaluableAI(token) if token else EvaluableAI()

    def chat(self, *args, **kwargs) -> ChatCompletionResponse:
        local_evaluableai_params = self.evaluableai_params.copy()
        ground_truth = kwargs.pop("ground_truth", None)
        if ground_truth:
            local_evaluableai_params["ground_truth"] = ground_truth

        try:
            start_time = time.time()
            chat_completion = super().chat(*args, **kwargs)
            end_time = time.time()
            local_evaluableai_params["time_taken"] = round((end_time - start_time) * 1000, 3)
            response_data = chat_completion

            skip_submit = local_evaluableai_params.pop("skip_submit", None)
            if skip_submit:
                return chat_completion

            request_data = self.handle_kwargs_for_chat(**kwargs)

            if local_evaluableai_params.get("async"):
                threading.Thread(target=lambda: asyncio.run(
                    self.post_to_server_async(request_data, response_data, local_evaluableai_params))).start()
            else:
                self.post_to_server(request_data, response_data, local_evaluableai_params)

            return chat_completion
        except MistralException:
            raise
        except Exception as e:
            raise EvaluableAIError(f"Failed during Mistral chat completion: {str(e)}")

    def post_to_server(self, request_data: Dict[str, Any], response_data: ChatCompletionResponse,
                       local_evaluableai_params: Dict[str, Any]) -> None:
        sampling_rate = local_evaluableai_params.pop("sampling", None)
        sampling_flag = is_selected_for_eval(sampling_rate) if sampling_rate is not None else True
        local_evaluableai_params["sampling_flag"] = sampling_flag

        endpoint = config['mistral_submit_data']
        if local_evaluableai_params.get("eval") and sampling_flag:
            endpoint = config['mistral_submit_data_and_eval']

        body = {
            "mistralai_request": request_data,
            "mistralai_response": response_data.dict() if response_data else None,
            "evaluableai_params": local_evaluableai_params
        }

        try:
            response = self.eval_client.make_request(method="POST", endpoint=endpoint, data=body)
            if response.status_code not in [200, 201]:
                raise EvaluableAIError(
                    f"Failed to post data to evaluable ai server: {response.status_code}, {response.text}")
        except Exception as e:
            raise EvaluableAIError(f"Failed to post data to evaluable ai server: {str(e)}")

    async def post_to_server_async(self, request_data: Dict[str, Any], response_data: ChatCompletionResponse,
                                   local_evaluableai_params: Dict[str, Any]) -> None:
        sampling_rate = local_evaluableai_params.pop("sampling", None)
        sampling_flag = is_selected_for_eval(sampling_rate) if sampling_rate is not None else True
        local_evaluableai_params["sampling_flag"] = sampling_flag

        endpoint = config['mistral_submit_data']
        if local_evaluableai_params.get("eval") and sampling_flag:
            endpoint = config['mistral_submit_data_and_eval']

        body = {
            "mistralai_request": request_data,
            "mistralai_response": response_data.dict() if response_data else None,
            "evaluableai_params": local_evaluableai_params
        }

        try:
            response = await self.eval_client.async_make_request(method="POST", endpoint=endpoint, data=body)
            if response.status_code not in [200, 201]:
                raise EvaluableAIError(
                    f"Failed to post data to evaluable ai server: {response.status_code}, {response.text}")
        except Exception as e:
            raise EvaluableAIError(f"Failed to post data to evaluable ai server: {str(e)}")

    def serialize_pydantic_model(self, model):
        """Serialize a Pydantic model to a dictionary, handling lists of models."""
        if isinstance(model, BaseModel):
            return model.dict()
        elif isinstance(model, list):
            return [self.serialize_pydantic_model(item) for item in model]
        return model

    def handle_kwargs_for_chat(self, **kwargs) -> Dict[str, Any]:
        """Serialize kwargs for the chat function, handling lists of Pydantic models."""
        return {key: self.serialize_pydantic_model(value) for key, value in kwargs.items()}
