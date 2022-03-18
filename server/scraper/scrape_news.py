import requests

from scraper.article_scraper import GoogleScraper
from scraper.page_processor import PageProcessor

def scrape_news_urls(queries, n_articles, pp_callback):
    scraper = GoogleScraper(verbose=True, log_prefix="    \033[1mscraper:\033[0m ")
    for i, query in enumerate(queries):
        print(f"\033[1mquery {i+1}/{len(queries)}\033[0m")
        urls = scraper.find_news_urls_for_query(query, n_articles)
        for url in urls:
            print(f"\r\033[K    \033[1mfetching\033[0m {url}", end="")
            page = requests.get(url).text
            processor = PageProcessor(page)
            pp_callback(processor, url, query)
        print()

