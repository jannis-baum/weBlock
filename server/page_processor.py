import sys
sys.path.append('../nlp')
from nlp import NLProcessor
from text_generator import TextGenerator
import json, re

class PageElement:
    def __init__(self, html):
        self.html = html
        self.text = re.sub('<.*>', '', html)
        self.context_elements = list()
        self.__similarity = None
        self.__sentiment = None
    
    def set_context(self, context_elements):
        self.context_elements = context_elements
    
    def similarity(self):
        if not self.__similarity:
            self.__similarity = NLProcessor.similarity(self.text)
        return self.__similarity
    
    def sentiment(self):
        if not self.__sentiment:
            self.__sentiment = NLProcessor.sentiment(self.text)
        return self.__sentiment['neg']
    
    def score(self):
        sim = (sum([context.similarity() for context in self.context_elements]) + self.similarity()) / len(self.context_elements)\
            if self.context_elements else self.similarity()
        return (sim + self.sentiment()) * self.sentiment() * 100
    
class PageProcessor:
    censoring_threshold = 10

    @staticmethod
    def setupCensoring(censoring_requirements, censoring_statement, generator_context):
        NLProcessor.set_similarity_data(censoring_requirements, censoring_statement)
        NLProcessor.ready()
        TextGenerator.ready(context_suffix=generator_context)

    def __init__(self, request):
        data = json.loads(request)
        self.should_generate = data['gen_text']
        self.__text_groups = dict()
        for tag, innerHTMLs in data['page'].items():
            self.__text_groups[tag] = list()
            for i, innerHTML in enumerate(innerHTMLs):
                self.__text_groups[tag].append(PageElement(innerHTML))
                if i:
                    context_elements = self.__text_groups[tag][i - (min(3, i)):i]
                    self.__text_groups[tag][i].set_context(context_elements)
    
    def censoring_edits(self):
        elements_flat = [elements for element_groups in self.__text_groups.values() for elements in element_groups]
        for element in elements_flat:
            if element.score() >= PageProcessor.censoring_threshold:
                if self.should_generate:
                    element.text = TextGenerator.generate(element.context_elements[-1].text if element.context_elements else '')
                element.html = '<div style="color: red !important;">' + element.text + '</div>'
                               
        return json.dumps({
            tag: [ element.html for element in elements]
        for tag, elements in self.__text_groups.items() })

