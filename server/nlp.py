import gensim.downloader as api
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet

class ABPP_NLP:
    __word_vectors = api.load("glove-wiki-gigaword-100")
    __filter_chars = ['.', ',', '?', ';', '"', '#', '\'', '!', '‘', '’', '“', '”', '…', ':']

    @staticmethod
    def __normal_set(words):
        normal = set()
        for word in [word.lower() for word in words]:
            normal.add(''.join([character for character in word if character not in ABPP_NLP.__filter_chars]))
        return normal
    
    @staticmethod
    def __synonyms(word):
        syns = []
        for syn in wordnet.synsets(word): 
            for lemm in syn.lemmas(): 
                syns += [lemm.name(), lemm.name() + 's']
        return set([syn for syn in ABPP_NLP.__normal_set(syns) if word not in syn] + [word, word + 's'])

    @staticmethod
    def similarity(crucial, statement, compare):
        crucial_syns = [ABPP_NLP.__synonyms(cruc) for cruc in crucial]
        compare_normal_set = ABPP_NLP.__normal_set(compare.split(' '))
        if not crucial and not crucial_syns & compare_normal_set:
            return float('inf')
        return ABPP_NLP.__word_vectors.wmdistance(compare, statement)

