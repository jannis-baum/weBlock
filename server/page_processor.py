from bs4 import BeautifulSoup
from nlp import NLProcessor

class PageElement:
    def __init__(self, element):
        self.__element = element
        self.__similarity = None
    
    def similarity(self):
        if not self.__similarity:
            self.__similarity = NLProcessor.similarity(self.__element.text)
        return self.__similarity
    
    def text(self):
        return self.__element.text

    def set_text(self, text):
        self.__element.string = text
        self.__similarity = None

    def string(self):
        return f'    text:\n        {self.__element.string}\n    similarity: {self.similarity()}'

class PageProcessor:
    relevant_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p']

    def __init__(self, html):
        self.__soup = BeautifulSoup(html, features='html.parser')
        self.__text_groups = dict(zip(PageProcessor.relevant_tags,
            [
                [PageElement(element) for element in self.__soup.find_all(key_tag) if element.text]
            for key_tag in PageProcessor.relevant_tags]
        ))
    
    def censor(self):
        for group in self.__text_groups.values():
            for element in group:
                element.set_text(element.text() + f' --- {element.similarity()}')
    
    def page(self):
        return str(self.__soup)

