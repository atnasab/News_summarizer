import newspaper
import time
from datetime import datetime
from newspaper import Article
import logging
import schedule
import json
import os

paper_sources = {
    'cnn': {
        'base_url': 'https://edition.cnn.com/',
        'categories_url': [
            'us',
            'us/crime-and-justice',
            'world',
            'world/africa',
            'world/europe',
            'business'
        ]
    },
    'techcrunch': {
        'base_url': 'https://techcrunch.com/',
        'categories_url': [
            'category/startups',
            'category/artificial-intelligence',
            'tag/apple'
        ]
    },
    'wired': {
        'base_url': 'https://www.wired.com/',
        'categories_url':[
            'category/security',
            'category/ideas',
            'category/big-story'
        ]
    },
    'espn': {
        'base_url': 'https://www.espn.in/',
        'categories_url': [
            'football',
            'cricket',
            'chess'
        ]
    }
}

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# url_dict = {source: {category for category in source_info['categories_url']} for source, source_info in paper_sources.items()}
total_articles = 0
max_articles_per_category = 10
max_total_articles = 200


logging.basicConfig(
    filename="article_fetcher.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_articles():
    global url_dict  
    logging.info("Fetching articles from sources...")
    
    url_dict = {source: {category: [] for category in source_info['categories_url']} for source, source_info in paper_sources.items()}

    for source, source_info in paper_sources.items():
        for category in source_info['categories_url']:  
            full_category_url = f"{source_info['base_url']}{category}/"
            logging.info(f"Fetching from: {full_category_url}")

            try:
                paper = newspaper.build(full_category_url, user_agent=user_agent, memoize_articles=False)             
                if not paper.articles:
                    logging.warning(f"No articles found for {source} in category {category}.")
                
                for article in paper.articles: 
                    if article.url not in url_dict[source][category]:
                        url_dict[source][category].append(article.url)

            except Exception as e:
                logging.error(f"Error fetching articles from {source} in category {category}: {e}")

            time.sleep(2)  

    for source, categories in url_dict.items():
        for category, urls in categories.items():
            logging.info(f"{source} - {category}: {len(urls)} articles found.")

    return url_dict


def download_articles(url_dict):
    global total_articles  
    article_contents = {source: {category: [] for category in paper_sources[source]['categories_url']} for source in paper_sources.keys()}
    fetched_urls = set()

    logging.info("Fetching article contents...")

    while total_articles < max_total_articles:
        for source in paper_sources.keys():
            if total_articles >= max_total_articles:
                break

            for category in paper_sources[source]['categories_url']:
                new_articles = [url for url in url_dict[source][category] if url not in fetched_urls][:max_articles_per_category]

                for url in new_articles:
                    if total_articles >= max_total_articles:
                        break
                    try:
                        start_time = time.time()
                        article = Article(url)
                        article.download()
                        article.parse()

                        top_image = article.top_image if article.top_image else None

                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        article_contents[source][category].append({
                            'url': url,
                            'title': article.title,
                            'image': top_image,
                            'text': article.text,
                            'authors': article.authors,
                            'publish_date': article.publish_date,
                            'fetched_at': timestamp
                        })
                        fetched_urls.add(url)
                        total_articles += 1
                        time_taken = time.time() - start_time
                        logging.info(f"Fetched {url} in {time_taken:.2f} seconds")

                        time.sleep(2)
                    except Exception as e:
                        logging.error(f"Error fetching {url} in category {category}: {e}")

    logging.info("Finished fetching articles.")
    return article_contents



def job():
    logging.info("Starting a new fetch job...")
    try:
        url_dict = fetch_articles()
        article_contents = download_articles(url_dict)
        save_articles(article_contents)
        logging.info(f"Total articles fetched this session: {total_articles}")
    except Exception as e:
        logging.error(f"Error in job: {e}")

if __name__ == "__main__":
    logging.info("Starting the articles fetcher...")
    job()
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)