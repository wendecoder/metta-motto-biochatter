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
collection = db["genes"]
collection2 = db["transcripts"]

# with open('genecode_nodes.metta', 'r') as file:
#     data = file.read()

# def extract_gene_and_transcript_info(content):
#     # Define the regex patterns for genes
#     gene_pattern = re.compile(r'\(gene (ENSG\d+)\)')
#     gene_name_pattern = re.compile(r'\(gene_name \(gene (ENSG\d+)\) ([\w\d]+)\)')

#     # Define the regex patterns for transcripts
#     transcript_pattern = re.compile(r'\(transcript (ENST\d+)\)')
#     transcript_name_pattern = re.compile(r'\(transcript_name \(transcript (ENST\d+)\) ([\w\d-]+)\)')

#     # Find all matches for genes
#     gene_matches = gene_pattern.findall(content)
#     gene_name_matches = gene_name_pattern.findall(content)

#     # Find all matches for transcripts
#     transcript_matches = transcript_pattern.findall(content)
#     transcript_name_matches = transcript_name_pattern.findall(content)

#     # Create dictionaries for quick lookup of gene and transcript names
#     gene_name_dict = {gene_id: gene_name for gene_id, gene_name in gene_name_matches}
#     transcript_name_dict = {transcript_id: transcript_name for transcript_id, transcript_name in transcript_name_matches}

#     # Create lists to store the results
#     gene_info = []
#     transcript_info = []

#     # Populate the gene_info list
#     for gene_id in gene_matches:
#         gene_info.append({
#             'gene_id': gene_id,
#             'gene_name': gene_name_dict.get(gene_id, ''),
#             'gene_description': ''
#         })

#     # Populate the transcript_info list
#     for transcript_id in transcript_matches:
#         transcript_info.append({
#             'transcript_id': transcript_id,
#             'transcript_name': transcript_name_dict.get(transcript_id, ''),
#             'transcript_description': ''
#         })

#     return gene_info, transcript_info

# gene_info, transcript_info = extract_gene_and_transcript_info(data)

# # Insert the gene_info into the genes collection
# if gene_info:
#     collection1.insert_many(gene_info)
#     print("Gene data inserted successfully.")

# # Insert the transcript_info into the transcripts collection
# if transcript_info:
#     collection2.insert_many(transcript_info)
#     print("Transcript data inserted successfully.")

def fetch_genecode_data(genecode_data):
    results = {}
    for genecode in genecode_data:
        ch = genecode.get_children()
        if str(ch[0]) == "transcript":
            results[str(ch[1])] = collection2.find_one({'transcript': str(ch[1])})
        else:
            results[str]

query = ['transcript', 'ENST00000533722']
# Genecode(query)