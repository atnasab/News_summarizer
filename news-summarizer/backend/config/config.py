from urllib.parse import quote_plus
# from config import MONGO_URI,DB_NAME,COLLECTION_NAME

username="nepalmadhav32454"
password="M@dh@v2020@"



encoded_username=quote_plus(username)
encoded_password=quote_plus(password)

MONGO_URI = (f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.jbm3k.mongodb.net/")

DB_NAME = "news_data"
COLLECTION_NAME = "portal_news"
summarized_article="summarized_news"