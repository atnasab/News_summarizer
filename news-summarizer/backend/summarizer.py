from pymongo import MongoClient
from config.config import MONGO_URI, DB_NAME, COLLECTION_NAME, summarized_article
from newspaper import Article
from transformers import pipeline
import logging

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

def extract_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        logging.error(f"Error extracting article from {url}: {e}")
        return None

def summarize_article(text):
    if not text or len(text.strip()) == 0:
        return "No text available for summarization."

    word_count = len(text.split())
    if word_count < 50:
        return text
    
    try:
        summary = summarizer(text, max_length=200, min_length=15, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        logging.error(f"Error during summarization: {e}")
        return "Error summarizing article."

def fetch_urls_from_mongodb():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        urls = [article['url'] for article in collection.find({"url": {"$exists": True}})]
        logging.info(f"Fetched {len(urls)} article URLs from MongoDB.")
        return urls
    except Exception as e:
        logging.error(f"Error fetching article URLs from DB: {e}")
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

    urls = fetch_urls_from_mongodb()
    if not urls:
        logging.info("No URLs found for summarization.")
        return

    summaries = []

    for url in urls:
        text = extract_article_text(url)
        if text:
            try:
                summary = summarize_article(text)
                summaries.append({'url': url, 'summary': summary})
                logging.info(f"Summarized article: {url}")
            except Exception as e:
                logging.error(f"Error summarizing article {url}: {e}")
        else:
            logging.warning(f"Skipping invalid article: {url}")

    if summaries:
        save_summaries_to_mongodb(summaries)

    logging.info("Summarization process completed.")

if __name__ == "__main__":
    main()
