from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import urllib.parse
import os
load_dotenv()

# Load the .emv file
load_dotenv()
            
# Get the MongoDB connection credential from environment variable(.env) file
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")

# Encode credentials to handle special characters
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)

# Construct the MongoDB connection URL
MONGO_DB_URL=f"mongodb+srv://{encoded_username}:{encoded_password}@{cluster}/?appName=Cluster0"


# Create a new client and connect to the server
client = MongoClient(MONGO_DB_URL, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)