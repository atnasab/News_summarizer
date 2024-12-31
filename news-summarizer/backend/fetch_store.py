import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from config.config import MONGO_URI,DB_NAME,COLLECTION_NAME
# from summarizer import summarize_text

def fetch_news(url,headline_selector,content_selector, max_articles=6):
    response=requests.get(url)
    if response.status_code!=200:
        print(f"Failed to fetch news site:{response.status_code}")
        return []
    soup=BeautifulSoup(response.content,"html.parser")
    headlines=soup.select(headline_selector)[:max_articles]

    articles=[]

    for headline in headlines:
        title=headline.text.strip()
        article_url=headline.get("href")
        if articles_url and not article_url.startwith("http"):
            article_url=url+article_url

        article_soup=BeautifulSoup(article_response.content,"html.parser")
        content= " ".join([p.text for p in article_soup.select(content_selector)])
        


        articles.append({
            "title":title,
            "url":article_url,
            "content":content
        })
        return articles



def insert_to_mongo():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    url=News_Site
    headline_selector=".article-title"
    content_selector=".article-content"

    articles = fetch_news(url,headline_selector,content_selector,max_articles=6)
    for article in articles:
        # summary= summarize_text(article["content"])
        document={
            "title":article["title"],
            "url":article["url"],
            "publishedAt":None,
            "summary":article["content"]
        }
        collection.insert_one(document)
    print("News articles summarized and stored.")
    client.close()
