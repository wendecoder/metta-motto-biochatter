from llama_index.llms.ollama import Ollama
from dotenv import load_dotenv
import os

load_dotenv()

base_url = os.getnev('BASE_URL')

class LlamaAgent:

    def __init__(self, model="llama3", request_timeout=120.0, base_url=base_url):
        self._model = model
        self._request_timeout = request_timeout
        self._base_url = base_url
        self._client = Ollama(model=self._model, request_timeout=self._request_timeout, base_url=self._base_url)

    def __call__(self, prompt):
        response = self._client.complete(prompt)
        return response