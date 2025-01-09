from fastapi import FastAPI,HTTPException
from typing import List
# from pydantic import BaseModel
from pymongo import MongoClient
from config.config import MONGO_URI, DB_NAME, COLLECTION_NAME
from pydantic import BaseModel

app = FastAPI()

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


class Article(BaseModel):
    title: str
    text: str
    authors: List[str]
    publish_date: List[str]
    fetched_at: List[str]

# class Article(BaseModel):
#     title=str
#     text=str
#     authors:List[str]
#     publish_date:List[str]
#     fetched_at:List[str]

# @app.route('/articles',response_model=list[Article])
# async def get_articles():
#     try:
#         articles=list(collection.find({}))
#         for article in articles:
#             article["_id"]=str(article["_id"])
#         return articles
#     except Exception as e:
#         raise HTTPException(status_code=500,detail=str(e))
#


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("R.png")

@app.get("/")
async def read_root():
    return {"message": "Welcome to my API"}

@app.get("/articles", response_model=List[Article])
async def get_articles():
    try:
        articles = list(collection.find({}))
        for article in articles:
            article["_id"] = str(article["_id"])
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)
