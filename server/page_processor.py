from bs4 import BeautifulSoup

class PageProcessor:
    relevant_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p']

    def __init__(self, html):
        self.soup = BeautifulSoup(html, features='html.parser')
        self.paragraphs = [paragraph.text for paragraph in self.soup.find_all(PageProcessor.relevant_tags)]
        self.paragraphs = dict(zip(PageProcessor.relevant_tags, [
            [paragraph.text for paragraph in self.soup.find_all(key_tag)] for key_tag in PageProcessor.relevant_tags
        ]))

