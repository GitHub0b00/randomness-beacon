import hashlib
import time
import pymongo
import json
from db_var import *

# Define the file path which the file of interest is stored.
file_path = "data.json"

# Connect to the database
client = pymongo.MongoClient(ip_address)


# This function computes the hash of all the texts in JSON file defined in the file path.
def calculate_file_hash(file_path):
    try:
        with open(file_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        return file_hash
    except FileNotFoundError:
        return None


# The following loop checks if there is a change in the hash of the file defined in the file path.
last_hash = calculate_file_hash(file_path)
while True:
    current_hash = calculate_file_hash(file_path)
    if (current_hash is not None) and (current_hash != last_hash):
        with open(file_path) as file:
            dic_cur = json.load(file)
        client[database_name][collection_name].insert_one(dic_cur)
        print("New pulse is found")
        last_hash = current_hash
    time.sleep(0.5)
