from pymongo import MongoClient
import re

password = 'fita1234'
name = "wenonezra258"
cluster_address = "cluster0.jwwwq0y.mongodb.net"
dbs_name = "atomspace"

uri = f"mongodb+srv://{name}:{password}@{cluster_address}/{dbs_name}?retryWrites=true&w=majority&appName=Cluster0"
try:
    client = MongoClient(uri)
except Exception as e:
    print(f"Error: {e}")

# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(f"Error: {e}")

db = client[dbs_name]
collection = db["protein"]


with open('protein_nodes.metta', 'r') as file:
    data = file.read()

def extract_protein_info(content):
    # Define the regex patterns
    protein_pattern = re.compile(r'\(protein (\w+)\)')
    name_pattern = re.compile(r'\(name \(protein (\w+)\) ([\w\d_]+)\)')

    # Find all matches
    protein_matches = protein_pattern.findall(content)
    name_matches = name_pattern.findall(content)

    # Create a dictionary to store the results
    protein_info = {}

    for protein_id in protein_matches:
        protein_info[protein_id] = {'name': None, 'description': ''}

    for match in name_matches:
        protein_id, protein_name = match
        if protein_id in protein_info:
            protein_info[protein_id]['name'] = protein_name

    return protein_info

# Extract protein info
protein_info = extract_protein_info(data)

print(protein_info)
