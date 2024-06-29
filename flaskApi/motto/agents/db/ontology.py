import re
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Replace with your actual username and password
username = "wenonezra258"
password = "fita1234"  # URL encode the password if needed
db_name = "atomspace"
# Alternative connection string without DNS seedlist format
uri = f"mongodb+srv://{username}:{password}@cluster0.jwwwq0y.mongodb.net/{db_name}"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(f"Error: {e}")

db = client[db_name]
collection = db["ontology_terms"]

def get_ontology_term(ontology_term):
    # print(f"Searching for ontology term: {ontology_term}")
    term = collection.find_one({'ontology_term': ontology_term}, {'_id': 0})
    # print(f"Result for {ontology_term}: {term}")
    if term:
        return term
    else:
        return {"ontology_term": ontology_term, "term_name": None, "description": "Not found"}

def fetch_ontology_terms(ontology_terms):
    results = {}
    for term in ontology_terms:
        results[term] = get_ontology_term(term)
    return results
