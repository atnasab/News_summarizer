from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pymongo import MongoClient
from config.config import MONGO_URI, DB_NAME, COLLECTION_NAME, summarized_article
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Restricting to needed methods
    allow_headers=["Content-Type", "Authorization"],
)

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
summary_news = db[summarized_article]

class Article(BaseModel):
    title: str
    text: str
    authors: List[str]
    publish_date: Optional[List[str]] = []
    fetched_at: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the news API"}

@app.get("/articles", response_model=List[Article])
async def get_articles():
    try:
        articles = list(collection.find({}))

        formatted_articles = []
        for article in articles:
            article["_id"] = str(article["_id"])  

            if isinstance(article.get("publish_date"), datetime):
                article["publish_date"] = [article["publish_date"].isoformat()]
            elif not isinstance(article.get("publish_date"), list):
                article["publish_date"] = []

            formatted_articles.append(article)

        return formatted_articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching articles: {str(e)}")

class Summary(BaseModel):
    original_id: str
    summary: str
    title: Optional[str] = ""
    url: Optional[str] = ""
    category: Optional[str] = ""
    image: Optional[str] = ""

@app.get("/summarized-news", response_model=List[Summary])
async def get_summarized_news():
    try:
        summaries = list(summary_news.find())

        if not summaries:
            print("No data found in the summarized news collection...!!!!")

        summarized_list = []

        for summary in summaries:
            print(f"Retrieved summary: {summary}")  # Debugging

            if "_id" in summary and "summary" in summary:
                summarized_list.append({
                    "original_id": str(summary["_id"]),  # FIXED HERE
                    "summary": summary.get("summary", ""), 
                    "title": summary.get("title", ""),
                    "url": summary.get("url", ""),
                    "category": summary.get("category", ""),
                    "image": summary.get("image", "")
                })
            else:
                print(f"Missing keys in summary: {summary}")

        return summarized_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching summaries: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)