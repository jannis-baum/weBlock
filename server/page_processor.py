from bs4 import BeautifulSoup
from nlp import NLProcessor
import json

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

    def content(self):
        return ''.join([str(sub_element) for sub_element in self.__element])

class PageProcessor:
    __relevant_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p']
    __censor_threshold = 0
    __key_tag = 'tag'
    __key_edits = 'edits'
    __key_index = 'index'
    __key_innerHTML = 'innerHTML'

    @staticmethod
    def setupNLP(censoring_requirements, censoring_statement):
        NLProcessor.set_similarity_data(censoring_requirements, censoring_statement)
        NLProcessor.ready()

    def __init__(self, html):
        self.__soup = BeautifulSoup(html, features='html.parser')
        self.__text_groups = dict(zip(PageProcessor.__relevant_tags,
            [
                [PageElement(element) for element in self.__soup.find_all(key_tag) if element.text]
            for key_tag in PageProcessor.__relevant_tags]
        ))
    
    def censored(self):
        return json.dumps([ {
                PageProcessor.__key_tag: tag,
                PageProcessor.__key_edits: [ {
                        PageProcessor.__key_index: idx,
                        PageProcessor.__key_innerHTML: element.content() + f' <b>{element.similarity()}</b>'
                    } for idx, element in enumerate(self.__text_groups[tag]) if element.similarity() > PageProcessor.__censor_threshold
                ]
            } for tag in PageProcessor.__relevant_tags
        ])
    
    def page(self):
        return str(self.__soup)

