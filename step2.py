import os
import json
import hashlib
from datetime import datetime
from pymongo import MongoClient

# Function to connect to MongoDB
def connect_to_mongodb():
    # Connect to MongoDB running on localhost
    client = MongoClient('mongodb://localhost:27017/')
    db = client['linkstore']  # Create or connect to 'linkstore' database
    return db

def extract_info(json_file, category):
    try:
        with open(json_file, 'r') as f:
            data_list = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading JSON file '{json_file}': {e}")
        return []

    info_list = []
    counter = 0

    for data in data_list:
        link_hash = hashlib.sha256(data.get("link", "").encode()).hexdigest()
        id_with_counter = f"{link_hash[:16]}_{counter}"
        published_time = data.get("published_time", "")
        if published_time:
            try:
                published_time = datetime.strptime(published_time, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                published_time = None

        info = {
            "title": data.get("title", ""),
            "link": data.get("link", ""),
            "displayLink": data.get("displayLink", ""),
            "snippet": data.get("snippet", ""),
            "formattedUrl": data.get("formattedUrl", ""),
            "category": category,  # Include category in extracted information
            "id": id_with_counter,
            "published_time": published_time
        }

        counter += 1

        pagemap = data.get("pagemap", {})
        if "metatags" in pagemap:
            info["metatags"] = pagemap["metatags"][0] if pagemap["metatags"] else {}
        else:
            info["metatags"] = {}

        info_list.append(info)

    return info_list

def process_files(directory):
    db = connect_to_mongodb()
    for filename in os.listdir(directory):
        if filename.startswith("Google_Search_Result_") and filename.endswith(".json"):
            category = filename.split("_")[3].split(".")[0]  # Extract category from filename
            collection_name = f'{category}'  # Create collection name based on category
            collection = db[collection_name]  # Get or create the collection
            json_file = os.path.join(directory, filename)
            info_list = extract_info(json_file, category)  # Pass category to extract_info function
            if info_list:
                collection.insert_many(info_list)

if __name__ == "__main__":
    process_files(".")
