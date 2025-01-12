import json
import os
from raw_data import fetch_articles, download_articles
from pymongo import MongoClient
from bson import ObjectId
from urllib.parse import quote_plus


username="nepalmadhav32454"
password="M@dh@v2020@"



encoded_username=quote_plus(username)
encoded_password=quote_plus(password)

MONGO_URI = (f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.jbm3k.mongodb.net/")
DB_NAME = "news_data"
COLLECTION_NAME = "portal_news"


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


    for source, articles in data.items():
        for article in articles:
            collection.insert_one(article)
        print(f"Articles from {source} inserted into MongoDB collection: {COLLECTION_NAME}")


 

if __name__ == "__main__":

    url_dict = fetch_articles()
    article_contents = download_articles(url_dict)
    save_articles_to_cache(article_contents)


    insert_data_to_mongodb(article_contents)