from nlp import NLProcessor
import json, re

class PageElement:
    def __init__(self, html):
        self.html = html
        self.text = re.sub('<.*>', '', html)
        self.__context_elements = list()
        self.__similarity = None
        self.__sentiment = None
    
    def set_context(self, context_elements):
        self.__context_elements = context_elements
    
    def similarity(self):
        if not self.__similarity:
            self.__similarity = NLProcessor.similarity(self.text)
        return self.__similarity
    
    def sentiment(self):
        if not self.__sentiment:
            self.__sentiment = NLProcessor.sentiment(self.text)
        return self.__sentiment['neg']
    
    def score(self):
        sim = (sum([context.similarity() for context in self.__context_elements]) + self.similarity()) / len(self.__context_elements)\
            if self.__context_elements else self.similarity()
        print(self.__context_elements)
        return (sim + self.sentiment()) * self.sentiment() * 100
    
class PageProcessor:
    @staticmethod
    def setupNLP(censoring_requirements, censoring_statement):
        NLProcessor.set_similarity_data(censoring_requirements, censoring_statement)
        NLProcessor.ready()

    def __init__(self, request):
        self.__text_groups = dict()
        for tag, innerHTMLs in json.loads(request).items():
            self.__text_groups[tag] = list()
            for i, innerHTML in enumerate(innerHTMLs):
                self.__text_groups[tag].append(PageElement(innerHTML))
                if i:
                    context_elements = self.__text_groups[tag][i - (min(3, i)):i]
                    self.__text_groups[tag][i].set_context(context_elements)
    
    def censoring_edits(self):
        return json.dumps({
            tag: [element.html
                + f' <code>score: {element.score():.2f}</code>'
                for element in elements]
            for tag, elements in self.__text_groups.items()
        })

