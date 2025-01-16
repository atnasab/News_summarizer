from transformers import pipeline
from pymongo import MongoClient
from config.config import MONGO_URI, DB_NAME, COLLECTION_NAME, summarized_article

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
summary_news = db[summarized_article]

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_articles():
    articles = collection.find()
    for article in articles:
        text = article.get("text")
        if text:
            # Truncate text if it exceeds the model's token limit
            tokens = summarizer.tokenizer.encode(text, return_tensors="pt")
            if tokens.size(1) > 1024:
                print(f"Truncating article {article['_id']} to fit model input")
                truncated_text = summarizer.tokenizer.decode(tokens[0, :1024], skip_special_tokens=True)
            else:
                truncated_text = text

            try:
                # Generate the summary
                summary = summarizer(truncated_text, max_length=100, min_length=30, do_sample=False)
                summarized_text = summary[0]["summary_text"]

                # Save the summary to the database
                summary_news.insert_one({
                    "original_id": article["_id"],
                    "summary": summarized_text
                })
                print(f"Summary of article {article['_id']} is: {summarized_text}")
            except Exception as e:
                print(f"Error summarizing article {article['_id']}: {e}")

if __name__ == "__main__":
    summarize_articles()
