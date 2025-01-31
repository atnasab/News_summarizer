import json
import os
from raw_data import fetch_articles, download_articles
from pymongo import MongoClient
import logging
from config.config import *

cache_file = "cached_articles.json"

logging.basicConfig(
    filename="article_storage.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_cached_articles():
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                logging.info("Loading cached articles from file")
                return json.load(f)
        except json.JSONDecodeError:
            logging.error("Error decoding JSON. Returning empty dictionary.")
        return {}
    return {}

def save_articles_to_cache(articles):
    try:
        with open(cache_file, "w") as f:
            json.dump(articles, f, indent=4, default=str)
        logging.info(f"Articles saved to cached file: {cache_file}")
    except Exception as e:
        logging.error(f"Error saving articles to cache: {e}")

def insert_data_to_mongodb(data):
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        total_inserted = 0
        total_existing = 0

        # Log the structure of the data for debugging
        logging.info(f"Data structure before processing: {data}")

        if not isinstance(data, dict):
            logging.error("Data is not a dictionary. Please check the structure of fetched articles.")
            return

        for source, articles in data.items():
            if not isinstance(articles, list):
                logging.error(f"Articles for source '{source}' is not a list. Skipping this source.")
                continue

            for article in articles:
                if not isinstance(article, dict):
                    logging.error(f"Article is not a dictionary: {article}. Skipping this article.")
                    continue

                if collection.find_one({"url": article['url']}) is None:
                    article['source'] = source
                    collection.insert_one(article)
                    logging.info(f"Inserted article from {source}: {article['url']}")
                    total_inserted += 1
                else:
                    logging.warning(f"Article already exists in database: {article['url']}")
                    total_existing += 1

        logging.info(f"Total articles inserted: {total_inserted}, Total existing articles: {total_existing}")
    except Exception as e:
        logging.error(f"Error inserting data into MongoDB: {e}")

if __name__ == "__main__":
    try:
        url_dict = fetch_articles()
        article_contents = download_articles(url_dict)

        # Log the structure of article_contents for debugging
        logging.info(f"Article contents structure: {article_contents}")

        save_articles_to_cache(article_contents)
        insert_data_to_mongodb(article_contents)

        logging.info("Article fetching and storage is completed.")
    except Exception as main_error:
        logging.error(f"Main error: {main_error}")