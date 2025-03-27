import os
import sys
import json
import urllib.parse
from dotenv import load_dotenv

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_convertor(self, csv_file_path):
        try:
            # Read the CSV file into a pandas DataFrame
            data = pd.read_csv(csv_file_path)
            
            # Drop the first column (index 0) if it is not needed
            data.reset_index(drop=True, inplace=True)

            # Convert the DataFrame to a JSON string and it to a list of dictionaries
            records = list(json.loads(data.T.to_json()).values())
            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def push_data_to_mongodb(self, records, database, collection_name):
        try:
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
            
            self.database = database
            self.collection_name = collection_name
            self.records = records
            
            # Create a MongoDB client
            self.mongo_client = MongoClient(MONGO_DB_URL, server_api=ServerApi('1'), tlsCAFile=ca)
            
            # Access the database and collection
            self.database = self.mongo_client[self.database]
            self.collection_name = self.database[self.collection_name]

            # Insert the records into the collection
            self.collection_name.insert_many(self.records)

            # Close the connection
            self.mongo_client.close()

            # Return the number of records inserted
            return (len(self.records))

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__=="__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "NetworkSecurity"
    COLLECTION_NAME = "NetworkData"
    
    # Initialize the NetworkDataExtract class 
    network_data_extractor = NetworkDataExtract()
    
    # Convert the CSV file to JSON using the csv_to_json_convertor method and print first record
    records = network_data_extractor.csv_to_json_convertor(FILE_PATH)
    print(records[0])
    
    # Push the data to MongoDB using the push_data_to_mongodb method and print the number of records inserted
    no_of_records = network_data_extractor.push_data_to_mongodb(records, DATABASE, COLLECTION_NAME)
    print(f"Number of records inserted: {no_of_records}")
