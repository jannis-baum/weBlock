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
    
    def score(self):
        return (self.similarity() + self.sentiment()) 
        return self.sentiment() * self.similarity() * 100
    
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
        rolling_sims = dict()
        for tag in self.__text_groups:
            rolling_sims[tag] = list()
            sim_vals = list()
            sim_avg = 0
            for i, tg in enumerate(self.__text_groups[tag]):
                if i > 2: sim_avg -= sim_vals.pop(0)
                sim_vals.append(tg.similarity())
                sim_avg += tg.similarity()
                print(len(sim_vals))
                rolling_sims[tag].append(sim_avg / len(sim_vals))

        return json.dumps({
            tag: [element.html
                + f' <code>score: {((rolling_sims[tag][i] + element.sentiment()) * element.sentiment() * 100):.2f}</code>'
                for i, element in enumerate(elements)]
            for tag, elements in self.__text_groups.items()
        })

