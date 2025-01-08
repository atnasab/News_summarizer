from fastapi import FastAPI,HTTPException
from typing import ClassVar
from pydantic import BaseModel
from pymongo import MongoClient
from config.config import MONGO_URI, DB_NAME, COLLECTION_NAME

app = FastAPI()

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


class Article(BaseModel):
    title=ClassVar[str]
    text=ClassVar[str]
    authors:list[str]
    publish_date:list[str]
    fetched_at:list[str]

@app.route('/articles',response_model=list[Article])
async def get_articles():
    try:
        articles=list(collection.find({}))
        for article in articles:
            article["_id"]=str(article["_id"])
        return articles
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)
