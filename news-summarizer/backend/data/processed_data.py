import json
import os
from raw_data import fetch_articles, download_articles
from pymongo import MongoClient
from config.config import MONGO_URI,DB_NAME,COLLECTION_NAME



cache_file = "cached_articles.json"

def load_cached_articles():
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error decoding JSON. Returning empty dictionary.")
        return {}
    return {}

def save_articles_to_cache(articles):
    with open(cache_file, "w") as f:
        json.dump(articles, f, indent=4, default=str)
        print(f"Articles saved to {cache_file}")

def insert_data_to_mongodb(data):
    client=MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]


    if isinstance(data,dict):
        collection.insert_one(data)
    elif isinstance(data,list):
        collection.insert_many(data)
    else:
        print("Data format is not supported")
    print(f"Data inserted into mongodb collection : {COLLECTION_NAME}")

if __name__ == "__main__":

    url_dict = fetch_articles()
    article_contents = download_articles(url_dict)
    save_articles_to_cache(article_contents)


    insert_data_to_mongodb(article_contents)