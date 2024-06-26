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
collection = db["pathways"]

# Initialize an empty list to store pathway data
pathway_data = []

# # Read the file and extract the pathway id and name
# with open('pathway_nodes.metta', 'r') as file:
#     lines = file.readlines()
#     for i in range(0, len(lines), 2):
#         pathway_id = lines[i].split()[1].strip(')')
#         name = lines[i + 1].split()[2].strip(')').replace('_', ' ')
#         pathway_data.append({
#             'pathway': pathway_id,
#             'name': name,
#             'description': ''
#         })

# # Insert the data into MongoDB
# collection.insert_many(pathway_data)

# print("Data inserted successfully into MongoDB")

def fetch_pathway_data(pathway_data):
    print("pathway_data", pathway_data)
    results = {}
    for pathway in pathway_data:
        ch = pathway.get_children()
        # print("second children", ch[1])
        pathway_data = collection.find_one({'pathway': str(ch[1])})
        print("pathway_data", pathway_data)
        results[str(ch[1])] = pathway_data
    if results:
        return results
    else:
        return "No pathway data found!"

