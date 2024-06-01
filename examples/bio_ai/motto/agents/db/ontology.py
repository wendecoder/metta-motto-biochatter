import re
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Replace with your actual username and password
username = "wenonezra258"
password = "fita1234"  # URL encode the password if needed
db_name = "ontology"
# Alternative connection string without DNS seedlist format
uri = f"mongodb+srv://{username}:{password}@cluster0.jwwwq0y.mongodb.net/{db_name}"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Error: {e}")

db = client[db_name]
collection = db["terms"]

'''
# Read the input data from a text file
with open('ontology_nodes.txt', 'r') as file:
    data = file.read()

# Function to parse the input data
def parse_data(data):
    terms = {}
    current_term = None

    for line in data.split('\n'):
        if line.strip() == '':
            continue
        
        match = re.match(r'\((\w+)\s+(GO:\d+)\)', line)
        if match:
            current_term = match.group(2)
            if current_term not in terms:
                terms[current_term] = {'ontology_term': current_term}
        elif current_term:
            match = re.match(r'\((\w+)\s+\(ontology_term\s+GO:\d+\)\s+(.*)\)', line)
            if match:
                key = match.group(1)
                value = match.group(2).replace('_', ' ')
                if key == 'synonyms':
                    value = value.strip('()').split()
                terms[current_term][key] = value

    return terms

# Parse the data
terms = parse_data(data)

# Convert the dictionary to a list of terms
terms_list = list(terms.values())

# Function to print specified fields of terms
def print_terms(terms):
    for term in terms:
        print({
            'ontology_term': term['ontology_term'],
            'term_name': term.get('term_name', 'N/A'),
            'description': term.get('description', 'N/A')
        })

# Print the first 3 and last 3 terms with only the specified fields
print("First 3 ontology terms:")
print_terms(terms_list[:3])

print("\nLast 3 ontology terms:")
print_terms(terms_list[-3:])

# Insert only specified fields into MongoDB
for term_data in terms_list:
    filtered_data = {
        'ontology_term': term_data['ontology_term'],
        'term_name': term_data.get('term_name', 'N/A'),
        'description': term_data.get('description', 'N/A')
    }
    collection.update_one({'ontology_term': filtered_data['ontology_term']}, {'$set': filtered_data}, upsert=True)

print("Data inserted into MongoDB successfully!")
'''

def get_ontology_term(ontology_term):
    print("get onto")
    term = collection.find_one({'ontology_term': ontology_term}, {'_id': 0})
    print("term",term)
    if term:
        return term
    else:
        return f"Ontology term {ontology_term} not found."

