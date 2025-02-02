import newspaper
import time
from datetime import datetime
from newspaper import Article
import logging
import schedule
import requests
from bs4 import BeautifulSoup

paper_sources = {
    'cnn': 'https://edition.cnn.com/',
    'fox news': 'https://www.foxnews.com/',
    'Sky News': 'https://news.sky.com/',
    'espn': 'https://www.espn.in/'
}

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
url_dict = {source: [] for source in paper_sources.keys()}
total_articles = 0
max_articles_per_category = 10
max_total_articles = 200

logging.basicConfig(
    filename="article_fetcher.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_categories(source_name, source_url):
    try:
        response = requests.get(source_url, headers={'User -Agent': user_agent})
        soup = BeautifulSoup(response.content, 'html.parser')

        categories = [a['href'] for a in soup.select('nav a[href^="/"]') if a.text.strip()]
        return categories
    except Exception as e:
        logging.error(f"Error fetching categories from {source_name}: {e}")
        return []

def fetch_articles():
    global url_dict  
    logging.info("Fetching articles from sources...")
    for source_name, source_url in paper_sources.items():
        categories = fetch_categories(source_name, source_url)

        for category_url in categories:
            full_category_url = f"{source_url}{category_url}"
            try:
                paper = newspaper.build(full_category_url, user_agent=user_agent, memoize_articles=False)
                if not paper.articles:
                    logging.warning(f"No articles found for {source_name} in category {category_url}.")
                for article in paper.articles: 
                    if article.url not in url_dict[source_name]:
                        url_dict[source_name].append(article.url)
            except Exception as e:
                logging.error(f"Error fetching articles from {source_name} in category {category_url}: {e}")

            time.sleep(2)

    for source, urls in url_dict.items():
        logging.info(f"{source}: {len(urls)} articles found.")

    return url_dict

def download_articles(url_dict):
    global total_articles  
    article_contents = {source: [] for source in paper_sources.keys()}
    fetched_urls = set()

    logging.info("Fetching article contents...")

    while total_articles < max_total_articles:
        for source in paper_sources.keys():
            if total_articles >= max_total_articles:
                break

            new_articles = [url for url in url_dict[source] if url not in fetched_urls][:max_articles_per_category]

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
                    article_contents[source].append({
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
                    logging.error(f"Error fetching {url} in category: {e}")

    logging.info("Finished fetching articles.")
    return article_contents

def job():
    logging.info("Starting a new fetch job...")
    try:
        url_dict = fetch_articles()
        article_contents = download_articles(url_dict)
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