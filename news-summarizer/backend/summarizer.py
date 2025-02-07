from pymongo import MongoClient
from config.config import MONGO_URI, DB_NAME, COLLECTION_NAME, summarized_article
from transformers import pipeline
import logging

# Configure logging
logging.basicConfig(
    filename="article_storage.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    logging.info("Summarization model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading summarization model: {e}")
    summarizer = None

def summarize_article(text):
    if not text:
        return "No text available for summarization."
    
    try:
        summary = summarizer(text, max_length=200, min_length=15, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        logging.error(f"Error during summarization: {e}")
        return "Error summarizing article."

def fetch_articles_from_mongodb():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        articles = list(collection.find({"text": {"$exists": True}}))

        logging.info(f"Fetched {len(articles)} articles from MongoDB.")
        return articles
    except Exception as e:
        logging.error(f"Error fetching articles from DB: {e}")
        return []
    finally:
        client.close()

def save_summaries_to_mongodb(summaries):
    try:
        client = MongoClient(MONGO_URI)  
        db = client[DB_NAME]
        summarized_collection = db[summarized_article]

        for summary in summaries:
            summarized_collection.update_one(
                {"url": summary['url']},
                {"$set": {"summary": summary['summary']}},
                upsert=True
            )

        logging.info("Summaries saved to MongoDB successfully.")
    except Exception as e:
        logging.error(f"Error saving summaries to MongoDB: {e}")
    finally:
        client.close()

def main():
    logging.info("Starting the summarization process...")

    articles = fetch_articles_from_mongodb()
    if not articles:
        logging.info("No articles found for summarization.")
        return

    summaries = []

    for article in articles:
        if 'text' in article and isinstance(article['text'], str) and len(article['text']) > 50:
            try:
                summary = summarize_article(article['text'])
                summaries.append({
                    'url': article['url'],
                    'summary': summary
                })
                logging.info(f"Summarized article: {article['url']}")
            except Exception as e:
                logging.error(f"Error summarizing article {article['url']}: {e}")
        else:
            logging.warning(f"Skipping invalid article: {article.get('url', 'Unknown URL')}")

    if summaries:
        save_summaries_to_mongodb(summaries)

    logging.info("Summarization process completed.")

if __name__ == "__main__":
    main()
