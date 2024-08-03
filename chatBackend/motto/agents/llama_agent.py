from llama_index.llms.ollama import Ollama

class LlamaAgent:

    def __init__(self, model="mistral", request_timeout=120.0, base_url="http://100.67.47.42:11434"):
        self._model = model
        self._request_timeout = request_timeout
        self._base_url = base_url
        self._client = Ollama(model=self._model, request_timeout=self._request_timeout, base_url=self._base_url)

    def __call__(self, prompt):
        response = self._client.complete(prompt)
        return response

