from flask import Flask, jsonify
from pymongo import MongoClient
from config.config import MONGO_URI, DB_NAME, COLLECTION_NAME

app = Flask(__name__)

@app.route("/news", methods=["GET"])
def get_news():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    articles = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB _id field
    client.close()
    return jsonify(articles)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
