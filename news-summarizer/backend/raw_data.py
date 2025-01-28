import newspaper
import time
from datetime import datetime
from newspaper import Article
import logging
import schedule

paper_sources = {
    'cnn': {
        'url': 'https://edition.cnn.com/',
        'categories': ['world', 'politics', 'business', 'health', 'entertainment', 'sports', 'us']
    },
    'fox news': {
        'url': 'https://www.foxnews.com/',
        'categories': ['politics', 'sports', 'entertainment', 'lifestyle']
    },
    'Sky News': {
        'url': 'https://news.sky.com/',
        'categories': ['uk', 'politics', 'world', 'us', 'money', 'science', 'climate and Tech', 'Programmes']
    },
    'espn': {
        'url': 'https://www.espn.in/',
        'categories': ['football', 'cricket', 'chess', 'ISL', 'F1', 'Hockey', 'NBA']
    }
}

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
url_dict = {source: {category: [] for category in details['categories']} for source, details in paper_sources.items()}
total_articles = 0
max_articles_per_category = 10
max_total_articles = 200

logging.basicConfig(
    filename="article_fetcher.log",
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s-%(message)s"
)


def fetch_articles():
    global url_dict  
    logging.info("Fetching articles from sources...")
    for source_name, details in paper_sources.items():
        source_url = details['url']
        for category in details['categories']:
            category_url = f"{source_url}{category}"
            try:
                paper = newspaper.build(category_url, user_agent=user_agent, memoize_articles=False)
                if not paper.articles:
                    print(f"No articles found for {source_name} in category {category}.")
                for article in paper.articles: 
                    if article.url not in url_dict[source_name][category]:
                        url_dict[source_name][category].append(article.url)
            except Exception as e:
                logging.error(f"Error fetching articles from {source_name} in category {category}: {e}")

            time.sleep(2)

    for source, categories in url_dict.items():
        for category, urls in categories.items():
            logging.info(f"{source} - {category}: {len(urls)} articles found.")

    return url_dict

def download_articles(url_dict):
    global total_articles  
    article_contents = {source: {category: [] for category in details['categories']} for source, details in paper_sources.items()}
    fetched_urls = set()

    logging.info("Fetching article contents...")

    while total_articles < max_total_articles:
        for source, details in paper_sources.items():
            for category in details['categories']:
                if total_articles >= max_total_articles:
                    break

                new_articles = [url for url in url_dict[source][category] if url not in fetched_urls][:max_articles_per_category]

                for url in new_articles:
                    if total_articles >= max_total_articles:
                        break
                    try:
                        start_time = time.time()
                        article = Article(url)
                        article.download()
                        article.parse()

                        top_image=article.top_image if article.top_image else None


                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        article_contents[source][category].append({
                            'url': url,
                            'title': article.title,
                            'category': category,
                            'image':top_image,
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