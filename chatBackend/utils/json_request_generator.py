import outlines
# login to access mistral model
import json
from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
from dotenv import load_dotenv

load_dotenv()

local_model_path = os.getenv('LOCAL_MODEL_PATH')

def use_outlines(user_question):
    prompt = f'''
    You are given a natural language query and your task is to generate a corresponding JSON request format. Below is an example of the JSON request structure:
    {{
      "requests": {{
        "nodes": [
          {{
            "node_id": "n1",
            "id": "",
            "type": "gene",
            "properties": {{}}
          }},
          {{
            "node_id": "n2",
            "id": "",
            "type": "transcript",
            "properties": {{}}
          }},
          {{
            "node_id": "n3",
            "id": "",
            "type": "protein",
            "properties": {{
              "protein_name": "MKKS"
            }}
          }}
        ],
        "predicates": [
          {{
            "type": "transcribed to",
            "source": "n1",
            "target": "n2"
          }},
          {{
            "type": "translates to",
            "source": "n2",
            "target": "n3"
          }}
        ]
      }}
    }}

    The nodes key contains the nodes the request is about, and the predicates key contains the mapping of relationships between the nodes in the nodes key.

    Here is an example of a natural language query: "What are the proteins that gene ENSG00000133710 codes for?"

    Your task is to convert the given natural language query into the corresponding JSON request format. Ensure the JSON request accurately reflects the information provided in the query, including the appropriate node types and relationships between them.

    Example Output:

    {{
      "requests": {{
        "nodes": [
          {{
            "node_id": "n1",
            "id": "ENSG00000133710",
            "type": "gene",
            "properties": {{}}
          }},
          {{
            "node_id": "n2",
            "id": "",
            "type": "transcript",
            "properties": {{}}
          }},
          {{
            "node_id": "n3",
            "id": "",
            "type": "protein",
            "properties": {{
              "protein_name": ""
            }}
          }}
        ],
        "predicates": [
          {{
            "type": "transcribed to",
            "source": "n1",
            "target": "n2"
          }},
          {{
            "type": "translates to",
            "source": "n2",
            "target": "n3"
          }}
        ]
      }}
    }}

    Note: The JSON request and natural language query provided are just examples. Use the given structure and information as a guide to generate similar JSON requests for other natural language queries.

    Below is the natural language query that you are going to generate the json format request for:

    {user_question}
    '''

    schema = '''{
    "title": "Requests",
    "type": "object",
    "properties": {
        "requests": {
        "type": "object",
        "properties": {
            "nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                "node_id": {
                    "type": "string",
                    "title": "Node ID"
                },
                "id": {
                    "type": "string",
                    "title": "ID",
                    "default": ""
                },
                "type": {
                    "type": "string",
                    "title": "Type",
                    "enum": ["gene", "transcript", "protein"]
                },
                "properties": {
                    "type": "object",
                    "title": "Properties"
                }
                },
                "required": ["node_id", "id", "type", "properties"]
            }
            },
            "predicates": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                "type": {
                    "type": "string",
                    "title": "Type",
                    "enum": ["transcribed to", "translates to"]
                },
                "source": {
                    "type": "string",
                    "title": "Source"
                },
                "target": {
                    "type": "string",
                    "title": "Target"
                }
                },
                "required": ["type", "source", "target"]
            }
            }
        },
        "required": ["nodes", "predicates"]
        }
    },
    "required": ["requests"]
    }
'''
    model = AutoModelForCausalLM.from_pretrained(local_model_path, local_files_only=True)
    generator = outlines.generate.json(model, schema)
    json_response = generator(prompt)
    return json_response