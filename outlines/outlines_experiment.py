import outlines
# login to access mistral model
import json
from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer


# Define the path to your local directory containing the model weights and config files
local_model_path = "/mnt/hdd_2/abdu/llama3/hf_weights"

def use_outlines():
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
}'''



    # Load the model
    model = AutoModelForCausalLM.from_pretrained(local_model_path, local_files_only=True)
    generator = outlines.generate.json(model, schema)
    character = generator("Give me a requests description")
    print(character)

use_outlines()

