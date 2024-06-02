from pymongo import MongoClient

password = 'fita1234'
name = "wenonezra258"
cluster_address = "cluster0.jwwwq0y.mongodb.net"
dbs_name = "genecode"

uri = f"mongodb+srv://{name}:{password}@{cluster_address}/{database_name}?retryWrites=true&w=majority&appName=Cluster0"
try:
    client = MongoClient(uri)
except Exception as e:
    print(f"Error: {e}")
db = client["gene"]
collection = db[dbs_name]
def Genecode(query):
    
    if query:
  
        datas = collection.find_one({str(query[0]):str(query[1])},{'_id': 0})
        # print("dsatass: ",datas)
        return datas

    else:
        return (f"The gene with {query} is none")

# query = ['transcript', 'ENST00000533722']
# Genecode(query)