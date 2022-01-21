import os
import urllib.request
from dotenv import load_dotenv
from page_processor import PageProcessor
from article_scraper import GoogleScraper
from database import Database
from nlp import NLProcessor

if __name__ == '__main__':
    load_dotenv()
    topic = os.getenv('SEARCH_QUERY')
    urls = GoogleScraper.find_urls_for_query(topic)
    GoogleScraper.quit()
    for url in urls:
        page = urllib.request.urlopen(url)
        processor = PageProcessor(page.read().decode("utf8"))
        page.close()
        summarization = NLProcessor.summarize(processor.get_fulltext())
        # summarization: [(sentence: String, score: Float)]
        # keep track of scores in database?
        # Database.insert([url, summarization, topic])

