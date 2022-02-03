from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

class GoogleScraper:
    __opts = Options();# __opts.headless = True
    __driver = None

    @staticmethod
    def __get_driver():
        if not GoogleScraper.__driver: GoogleScraper.__driver = webdriver.Firefox(options=GoogleScraper.__opts)
        return GoogleScraper.__driver

    @staticmethod
    def quit():
        GoogleScraper.__get_driver().quit()

    @staticmethod
    def find_urls_for_query(query):
        GoogleScraper.__get_driver().get('https://google.com')
        try:
            agree_btn = next(btn for btn in GoogleScraper.__get_driver().find_elements(By.TAG_NAME, 'button') if 'Ich stimme zu' in btn.get_attribute('innerHTML'))
            agree_btn.click()
        except: pass
        search_bar = GoogleScraper.__get_driver().find_element(By.XPATH, '//input[@title="Suche"][@name="q"]')
        search_bar.send_keys(query + Keys.ENTER)

        fetch_results = lambda: [a_tag.get_attribute('href') for a_tag in GoogleScraper.__driver.find_elements(By.XPATH, '//a/h3/..')]
        results = list()
        while not results:
            results = fetch_results()
        results_prev = list()
        while len(results_prev) < len(results):
            results_prev = results
            results = fetch_results()
            time.sleep(1)
        return results

    def find_news_htlms_for_query(query):
        GoogleScraper.__get_driver().get('https://news.google.com')
        try:
            agree_btn = next(btn for btn in GoogleScraper.__get_driver().find_elements(By.TAG_NAME, 'button') if 'I agree' in btn.get_attribute('innerHTML'))
            agree_btn.click()
        except: pass

        search_bar = GoogleScraper.__get_driver().find_element(By.XPATH, '//input[@value="Search for topics, locations & sources"]')

        action = webdriver.common.action_chains.ActionChains(GoogleScraper.__get_driver())
        action.move_to_element_with_offset(search_bar, 5, 5)
        action.click()
        action.send_keys("China censors content" + Keys.ENTER)
        action.perform()

        time.sleep(3)
        fetch_results = lambda: [a_tag.get_attribute('href') for a_tag in GoogleScraper.__get_driver().find_elements(By.XPATH, '//article[@ve-visible="true"]/a')][:10]
        results = list()
        while not results:
            results = fetch_results()
        results_prev = list()
        while len(results_prev) < len(results):
            results_prev = results
            results = fetch_results()
            time.sleep(1)

        htmls = list()
        for url in results:
            GoogleScraper.__get_driver().get(url)
            time.sleep(3)
            htmls.append(GoogleScraper.__get_driver().page_source)
        return htmls

