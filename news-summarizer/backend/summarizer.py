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
        summary = summarizer(text, max_length=300, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        logging.error(f"Error during summarization: {e}")
        return "Error summarizing article."

def fetch_articles_from_mongodb():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        articles = list(collection.find({"url": {"$exists": True}}, {"url": 1, "title": 1, "image": 1, "category": 1, "_id": 0}))
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
                {"$set": {"summary": summary['summary'], "title": summary['title'], "image": summary['image'], "category": summary['category']}},
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
        url, title, image, category = article.get("url"), article.get("title"), article.get("image"), article.get("category")
        text = extract_article_text(url)
        if text:
            try:
                summary = summarize_article(text)
                summaries.append({
                    'url': url,
                    'summary': summary,
                    'title': title,
                    'image': image,
                    'category': category
                })
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
