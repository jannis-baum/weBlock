import gensim.downloader as api
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet

class NLProcessor:
    __filter_chars = ['.', ',', '?', ';', '"', '#', '\'', '!', '‘', '’', '“', '”', '…', ':']
    __word_vectors = None
    __sim_requirements = None
    __sim_statement = ''

    @staticmethod
    def __normal_set(words):
        normal = set()
        for word in [word.lower() for word in words]:
            normal_word = ''.join([character for character in word if character not in NLProcessor.__filter_chars])
            normal.update(normal_word.split('_'))
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
        if not NLProcessor.__word_vectors:
            NLProcessor.__word_vectors = api.load("glove-wiki-gigaword-100")
        return NLProcessor.__word_vectors
    
    @staticmethod
    def set_word_vectors(vectors):
        NLProcessor.__word_vectors = vectors

    @staticmethod
    def set_similarity_data(requirements, statement):
        NLProcessor.__sim_requirements = set.union(*[
            NLProcessor.__synonyms(req) for req in requirements
        ]) if requirements else None
        NLProcessor.__sim_statement = statement

    @staticmethod
    def similarity(phrase):
        if NLProcessor.__sim_requirements:
            compare_normal_set = NLProcessor.__normal_set(phrase.split(' '))
            if not (NLProcessor.__sim_requirements & compare_normal_set):
                return 0
        return 1 / NLProcessor.__get_word_vectors().wmdistance(phrase, NLProcessor.__sim_statement)
    
