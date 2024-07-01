from flask import Flask, jsonify, request
from hyperon import MeTTa, ExpressionAtom, OperationAtom
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


metta = MeTTa()

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask API!"

@app.route('/api/question', methods=['POST'])
def answer_question():
    data = request.get_json()
    question = data.get('question')
    
    # Simple logic to determine the response (you can replace this with any logic or integration)
    mettaresponse = mettaResponse(question)
    response = str(mettaresponse[2][0]).strip('"')

    return jsonify(response=response)

def mettaResponse(user_message):
    response = metta.run(f'''
                !(import! &self motto)
                !(bind! &bioaiagent (Agent bio_ai_agent.msa))
                !(llm &bioaiagent (user "{user_message}"))
            ''')
    print(response)
    return response
if __name__ == '__main__':
    app.run(debug=True)
