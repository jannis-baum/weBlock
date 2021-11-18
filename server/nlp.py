import gensim.downloader as api
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet

class NLProcessor:
    __filter_chars = ['.', ',', '?', ';', '"', '#', '\'', '!', '‘', '’', '“', '”', '…', ':']

    @staticmethod
    def __normal_set(words):
        normal = set()
        for word in [word.lower() for word in words]:
            normal.add(''.join([character for character in word if character not in NLProcessor.__filter_chars]))
        return normal
    
    @staticmethod
    def __synonyms(word):
        syns = []
        for syn in wordnet.synsets(word): 
            for lemm in syn.lemmas(): 
                syns += [lemm.name(), lemm.name() + 's']
        return set([syn for syn in NLProcessor.__normal_set(syns) if word not in syn] + [word, word + 's'])

    @staticmethod
    def __get_word_vectors():
        if not hasattr(NLProcessor, 'word_vectors'):
            NLProcessor.word_vectors = api.load("glove-wiki-gigaword-100")
        return NLProcessor.word_vectors

    @staticmethod
    def similarity(requirements, statement, compare):
        if not requirements:
            return float('inf')
        req_syns = set.union(*[NLProcessor.__synonyms(req) for req in requirements])
        compare_normal_set = NLProcessor.__normal_set(compare.split(' '))
        if not (req_syns & compare_normal_set):
            return float('inf')
        return NLProcessor.__get_word_vectors().wmdistance(compare, statement)
    
