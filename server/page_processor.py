from nlp import NLProcessor
import json, re

class PageElement:
    def __init__(self, html):
        self.html = html
        self.text = re.sub('<.*>', '', html)
        self.__similarity = None
        self.__sentiment = None
    
    def similarity(self):
        if not self.__similarity:
            self.__similarity = NLProcessor.similarity(self.text)
        return self.__similarity
    
    def sentiment(self):
        if not self.__sentiment:
            self.__sentiment = NLProcessor.sentiment(self.text)
        return self.__sentiment['neg']
    
class PageProcessor:
    @staticmethod
    def setupNLP(censoring_requirements, censoring_statement):
        NLProcessor.set_similarity_data(censoring_requirements, censoring_statement)
        NLProcessor.ready()

    def __init__(self, request):
        self.__text_groups = {
            tag: [PageElement(innerHTML) for innerHTML in innerHTMLs]
            for tag, innerHTMLs in json.loads(request).items()
        }
    
    def censoring_edits(self):
        return json.dumps({
            tag: [element.html + f' <code>sim: {element.similarity():.2f} sent: {element.sentiment()}</code>' for element in elements]
            for tag, elements in self.__text_groups.items()
        })

