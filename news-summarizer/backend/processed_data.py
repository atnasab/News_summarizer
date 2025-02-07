import json
import os
from datetime import datetime
from pymongo import MongoClient
import logging
from config.config import MONGO_URI, DB_NAME, COLLECTION_NAME
from raw_data import fetch_articles, download_articles  

cache_file = "cached_articles.json"

logging.basicConfig(
    filename="article_storage.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def datetime_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()  
    raise TypeError("Type not serializable")

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
            json.dump(articles, f, indent=4, default=datetime_converter)  
        logging.info(f"Articles saved to cache file: {cache_file}")
    except Exception as e:
        logging.error(f"Error saving articles to cache: {e}")

def insert_data_to_mongodb(data):
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        total_inserted = 0
        total_existing = 0

        logging.info(f"Processing data structure: {json.dumps(data, indent=4, default=datetime_converter)}")

        if not isinstance(data, dict):
            logging.error("Data is not a dictionary. Please check the structure of fetched articles.")
            return

        for source, categories in data.items():
            if not isinstance(categories, dict):
                logging.error(f"Categories for source '{source}' is not a dictionary. Skipping this source.")
                continue

            for category, article_list in categories.items():
                if not isinstance(article_list, list):
                    logging.error(f"Article list for category '{category}' in source '{source}' is not a list. Skipping this category.")
                    continue

                for article in article_list:
                    if not isinstance(article, dict):
                        logging.error(f"Invalid article format: {article}. Skipping this article.")
                        continue

                    if 'url' not in article or 'title' not in article:
                        logging.error(f"Missing required fields in article: {article}. Skipping.")
                        continue

                    if collection.find_one({"url": article['url']}) is None:
                        article['source'] = source
                        article['category'] = category
                        collection.insert_one(article)
                        logging.info(f"Inserted article from {source} ({category}): {article['url']}")
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

        logging.info(f"Fetched article structure: {json.dumps(article_contents, indent=4, default=datetime_converter)}")

        save_articles_to_cache(article_contents)
        insert_data_to_mongodb(article_contents)

        logging.info("Article fetching and storage completed successfully.")
    except Exception as main_error:
        logging.error(f"Main error: {main_error}")
