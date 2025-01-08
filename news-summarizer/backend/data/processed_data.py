import json
import os

cache_file = "cached_articles.json"

def load_cached_articles():
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error decoding JSON. Returning empty dictionary.")
        return {}
    return {}

def save_articles_to_cache(articles):
    with open(cache_file, "w") as f:
        json.dump(articles, f, indent=4, default=str)
        print(f"Articles saved to {cache_file}")

if __name__ == "__main__":
    from raw_data import fetch_articles, download_articles

    url_dict = fetch_articles()
    article_contents = download_articles(url_dict)
    save_articles_to_cache(article_contents)