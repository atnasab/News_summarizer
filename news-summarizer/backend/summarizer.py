from pymongo import MongoClient
from config.config import MONGO_URI, DB_NAME, COLLECTION_NAME, summarized_article
from newspaper import Article
import logging

logging.basicConfig(
    filename="article_storage.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
summary_news = db[summarized_article]

def summarize_articles(max_sentences=4):
    articles = collection.find()
    for article in articles:
        url = article.get("url")
        category = article.get("category", "Uncategorized") 
        if url:
            try:
                article_instance = Article(url)
                article_instance.download()
                article_instance.parse()

                article_text = article_instance.text
                word_count = len(article_text.split())

                if word_count < 50:
                    logging.info(f"Article {article['_id']} is too short for summarization. Word count: {word_count}")
                    continue

                article_instance.nlp()
                summarized_text = article_instance.summary
                summarized_sentences = summarized_text.split('. ')
                limited_summary = '. '.join(summarized_sentences[:max_sentences]) + ('.' if summarized_sentences else '')

                title = article_instance.title or "No Title"  
                top_image = article_instance.top_image if article_instance.top_image else None

                if summary_news.find_one({"original_id": article["_id"]}) is None:
                    summary_news.insert_one({
                        "original_id": article["_id"],
                        'title': title,
                        'url': url,
                        'category': category,
                        'image': top_image,
                        "summary": limited_summary
                    })
                    logging.info(f"Summary of article {article['_id']} is: {limited_summary}")
                else:
                    logging.warning(f"Summary already exists for article: {article['_id']}")
            except Exception as e:
                logging.error(f"Error summarizing article {article['_id']}: {e}")

if __name__ == "__main__":
    summarize_articles(max_sentences=4)