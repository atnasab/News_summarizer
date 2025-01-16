from transformers import pipeline
from pymongo import MongoClient
from config.config import MONGO_URI, DB_NAME, COLLECTION_NAME, summarized_article

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
summary_news = db[summarized_article]

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str):
    
    tokens = summarizer.tokenizer.encode(text, return_tensors="pt")

    if tokens.size(1) > 1024:
        print(f"Truncating text to fit model input size.")
        truncated_tokens = tokens[0, :1024]
        truncated_text = summarizer.tokenizer.decode(truncated_tokens, skip_special_tokens=True)
    else:
        truncated_text = text

    summary = summarizer(truncated_text, max_length=200, min_length=30, do_sample=False)
    return summary[0]["summary_text"]

def summarize_articles():

    articles = collection.find()
    for article in articles:
        text = article.get("text")
        if text:
            try:
                summarized_text = summarize_text(text)
                summary_news.insert_one({
                    "original_id": article["_id"],
                    "summary": summarized_text
                })
                print(f"Summary of article {article['_id']} is: {summarized_text}")
            except Exception as e:
                print(f"Error summarizing article {article['_id']}: {e}")

if __name__ == "__main__":
    summarize_articles()
