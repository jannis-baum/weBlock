import os
from dotenv import load_dotenv

from article_scraper import GoogleScraper

if __name__ == '__main__':
    load_dotenv()
    urls = GoogleScraper.find_urls_for_query(os.getenv('SEARCH_QUERY'))
    GoogleScraper.quit()
    print(urls)

