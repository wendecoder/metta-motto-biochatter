from llama import LlamaAgent
from llama_index.llms.ollama import Ollama

def summarize_json_response(json_response):
    prompt = f'''
    You are given a json format information and your task is to summarize the information in the json and return the summary. Below is the json format information:
    {json_response}
    '''
    llm = Ollama(model="llama3", request_timeout=120.0, base_url="http://100.67.47.42:11434")
    response = llm.complete(prompt)
    return response.text