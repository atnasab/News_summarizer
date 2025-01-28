from fastapi import FastAPI, HTTPException
from typing import List
from pymongo import MongoClient
from config.config import MONGO_URI, DB_NAME, COLLECTION_NAME, summarized_article
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
summary_news = db[summarized_article]

class Article(BaseModel):
    title: str
    text: str
    authors: List[str]
    publish_date: List[str]
    fetched_at: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the news API"}

@app.get("/articles", response_model=List[Article])
async def get_articles():
    try:
        articles = list(collection.find({}))
        for article in articles:
            article["_id"] = str(article["_id"])
            if article.get("publish_date") is None:
                article["publish_date"] = []
            elif isinstance(article.get("publish_date"), datetime):
                article["publish_date"] = [article["publish_date"].isoformat()]
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class Summary(BaseModel):
    original_id: str
    summary: str
    title: str
    url: str
    category: str
    image: str

@app.get("/summarized-news", response_model=List[Summary])
def get_summarized_news():
    summaries = summary_news.find()
    summarized_list = []
    
    for summary in summaries:
        logging.info(f"Retrieved summary: {summary}")  # Log the retrieved summary
        
        if 'original_id' in summary and 'summary' in summary:
            summarized_list.append({
                'original_id': str(summary['original_id']),
                'summary': summary.get('summary', ''),  # Corrected this line
                'title': summary.get('title', ''),
                'url': summary.get('url', ''),
                'category': summary.get('category', ''),
                'image': summary.get('image', '')
            })
        else:
            print(f"Missing keys in summary: {summary}")
    
    return summarized_list

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)