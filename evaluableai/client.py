import json
import os
import httpx
import logging
from evaluableai.auth import Auth

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EvaluableAI:
    def __init__(self, token=None):
        with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as file:
            config = json.load(file)
        self.base_url = config.get("base_url")
        if token is None:
            token = os.getenv("EVALUABLEAI_API_KEY")
        if not token:
            raise ValueError("API token must be provided either as an argument or in the environment variable 'EVALUABLEAI_API_KEY'.")
        self.auth = Auth(token)

    def make_request(self, method="GET", endpoint="", data=None):
        """
        Synchronous request method.
        """
        headers = self.auth.get_headers()
        url = f"{self.base_url}{endpoint}"

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.request(method, url, headers=headers, json=data)
                if response.status_code not in [200, 201]:
                    logger.error(f"Request failed with status code: {response.status_code} - {response.text}")
                    response.raise_for_status()
                logger.info(f"Request to {url} completed with status code {response.status_code}")
                return response

        except httpx.RequestError as exc:
            logger.error(f"Request error occurred: {exc}")
            raise

class AsyncEvaluableAI:
    def __init__(self, token=None):
        with open(os.path.join(os.path.dirname(__file__), 'data.json'), 'r') as file:
            config = json.load(file)
        self.base_url = config.get("base_url")
        if token is None:
            token = os.getenv("EVALUABLEAI_API_KEY")
        if not token:
            raise ValueError("API token must be provided either as an argument or in the environment variable 'EVALUABLEAI_API_KEY'.")

        self.auth = Auth(token)

    async def async_make_request(self, method="GET", endpoint="", data=None):
        """
        Asynchronous request method.
        """
        headers = self.auth.get_headers()
        url = f"{self.base_url}{endpoint}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, headers=headers, json=data)
                if response.status_code not in [200, 201]:
                    logger.error(f"Request failed with status code: {response.status_code} - {response.text}")
                    response.raise_for_status()
                logger.info(f"Request to {url} completed with status code {response.status_code}")
                return response

        except httpx.RequestError as exc:
            logger.error(f"Request error occurred: {exc}")
            raise
