import os
import requests
from dotenv import load_dotenv
from page_processor import PageProcessor
from article_scraper import GoogleScraper
from database.database import Database
from nlp.nlp import NLProcessor

if __name__ == '__main__':
    load_dotenv()
    topic = os.getenv('SEARCH_QUERY')
    urls = GoogleScraper.find_urls_for_query(topic)
    GoogleScraper.quit()
    for url in urls:
        page = requests.get(url).text
        processor = PageProcessor(page)
        summarization = ''.join(NLProcessor.summarize(processor.get_fulltext()))
        print(summarization)
        Database.insert([url, summarization, topic])

