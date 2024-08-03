from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from .utils.json_request_generator import use_outlines
from .utils.generate_json_request_prompt import generate_json_request
from .utils.summarize_response_prompt import summarize_json_response
import requests

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')



app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask API!"

@app.route('/api/question', methods=['POST'])
def answer_question():
    data = request.get_json()
    question = data.get('question')
    
    json_request = generate_json_request(question)

     # Define the headers and payload for the POST request
    headers = {'Content-Type': 'application/json'}
    payload = {'requests': json_request}
    
    # Make the POST request to the /query endpoint
    annotation_response = requests.post('http://localhost:5000/query', headers=headers, json=payload)
    summarized_response = summarize_json_response(annotation_response)

    return jsonify(response=summarized_response)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
