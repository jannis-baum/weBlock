from nlp import NLProcessor
import json, re

class PageElement:
    def __init__(self, html):
        self.html = html
        self.text = re.sub('<.*>', '', html)
        self.__similarity = None
    
    def similarity(self):
        if not self.__similarity:
            self.__similarity = NLProcessor.similarity(self.text)
        return self.__similarity
    
class PageProcessor:
    __censor_threshold = 0

    @staticmethod
    def setupNLP(censoring_requirements, censoring_statement):
        NLProcessor.set_similarity_data(censoring_requirements, censoring_statement)
        NLProcessor.ready()

    def __init__(self, request):
        self.__text_groups = {
            tag: [PageElement(innerHTML) for innerHTML in innerHTMLs]
            for tag, innerHTMLs in json.loads(request)
        }
    
    def censoring_edits(self):
        return json.dumps({
            tag: [element.html + f' {element.similarity()}' for element in elements]
            for tag, elements in self.__text_groups
        })

