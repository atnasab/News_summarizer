import newspaper
import time
from datetime import datetime
from newspaper import Article

paper_sources = {
    'cnn': 'https://edition.cnn.com/',
    'fox news': 'https://www.foxnews.com/',
    'Sky News': 'https://news.sky.com/',
    'Foreign Policy': 'https://foreignpolicy.com/'
}

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
url_dict = {source: [] for source in paper_sources.keys()}
total_articles = 0
max_articles_per_source = 3
max_total_articles = 300

def fetch_articles():
    global url_dict  
    for source_name, source_url in paper_sources.items():
        try:
            paper = newspaper.build(source_url, user_agent=user_agent, memoize_articles=False)
            if not paper.articles:
                print(f"No articles found for {source_name}.")
            for article in paper.articles:
                if article.url not in url_dict[source_name]:
                    url_dict[source_name].append(article.url)
        except Exception as e:
            print(f"Error fetching articles from {source_name}: {e}")

        time.sleep(2)

    for source, urls in url_dict.items():
        print(f"{source}: {len(urls)}")

    return url_dict

def download_articles(url_dict):
    global total_articles  
    article_contents = {source: [] for source in paper_sources.keys()}
    fetched_urls = set()

    while total_articles < max_total_articles:
        for source in paper_sources.keys():
            if total_articles >= max_total_articles:
                break

            new_articles = [url for url in url_dict[source] if url not in fetched_urls][:max_articles_per_source]

            for url in new_articles:
                if total_articles >= max_total_articles:
                    break
                try:
                    start_time = time.time()
                    article = Article(url)
                    article.download()
                    article.parse()

                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    article_contents[source].append({
                        'url': url,
                        'title': article.title,
                        'text': article.text,
                        'authors': article.authors,
                        'publish_date': article.publish_date,
                        'fetched_at': timestamp
                    })
                    fetched_urls.add(url)
                    total_articles += 1
                    time_taken = time.time() - start_time
                    print(f"Fetched {url} in {time_taken:.2f} seconds")

                    time.sleep(2)
                except Exception as e:
                    print(f"Error fetching {url}: {e}")

    return article_contents

if __name__ == "__main__":
    url_dict = fetch_articles()
    article_contents = download_articles(url_dict)
    print(f"\nTotal articles fetched: {total_articles}")