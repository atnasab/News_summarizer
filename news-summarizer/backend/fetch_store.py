import requests
from pymongo import MongoClient
from config.config import MONGO_URI, NEWS_API_KEY, DB_NAME, COLLECTION_NAME
from summarizer import summarize_text

def fetch_news(api_key, query, page_size=10):
    url = "https://newsapi.org/v2/everything"
    params = {"q": query, "apiKey": api_key, "pageSize": page_size}
    response = requests.get(url, params=params)
    return response.json().get("articles", [])

def insert_to_mongo():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    articles = fetch_news(NEWS_API_KEY, "technology", page_size=5)
    for article in articles:
        content = article.get("description", "") + " " + article.get("content", "")
        summary = summarize_text(content)
        document = {
            "title": article.get("title"),
            "url": article.get("url"),
            "publishedAt": article.get("publishedAt"),
            "summary": summary
        }
        collection.insert_one(document)
    print("News articles summarized and stored.")
    client.close()
