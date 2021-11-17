from bs4 import BeautifulSoup
from nlp import NLProcessor

class PageElement:
    def __init__(self, text, censoring_requirements, censoring_statement):
        self.text = text
        self.similarity = NLProcessor.similarity(censoring_requirements, censoring_statement, self.text)
    
    def string(self):
        return f'    text:\n        {self.text}\n    similarity: {self.similarity}'

class PageProcessor:
    relevant_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p']

    def __init__(self, censoring_statement, censoring_requirements, html):
        self.soup = BeautifulSoup(html, features='html.parser')
        self.paragraphs = dict(zip(PageProcessor.relevant_tags,
            [
                [PageElement(element.text, censoring_requirements, censoring_statement) for element in self.soup.find_all(key_tag)]
            for key_tag in PageProcessor.relevant_tags]
        ))

