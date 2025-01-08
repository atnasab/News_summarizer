from urllib.parse import quote_plus
# from config import MONGO_URI,DB_NAME,COLLECTION_NAME

username="nepalmadhav32454"
password="M@dh@v2020@"



encoded_username=quote_plus(username)
encoded_password=quote_plus(password)

MONGO_URI = (f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.jbm3k.mongodb.net/")
# NEWS_API_KEY = "your_news_api_key_here"
# News_Site="cnn.com"
DB_NAME = "news_db"
COLLECTION_NAME = "raw_news"