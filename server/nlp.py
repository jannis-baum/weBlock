from os import fpathconf
import gensim.downloader as api
import nltk
from nltk.corpus import wordnet
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class NLProcessor:
    __filter_chars = ['.', ',', '?', ';', '"', '#', '\'', '!', '‘', '’', '“', '”', '…', ':', '_', '*'] 
    __stop_words_path = 'resources/stop_words_en.txt'
    __stop_words = None
    __word_vectors_id = 'word2vec-google-news-300'
    __word_vectors = None
    __sim_requirements = None
    __sim_statement = ''
    __sentimentIA = SentimentIntensityAnalyzer()

    @staticmethod
    def __get_stop_words():
        if not NLProcessor.__stop_words:
            with open(NLProcessor.__stop_words_path, 'r') as fp:
                NLProcessor.__stop_words = fp.read().split('\n')
        return NLProcessor.__stop_words

    @staticmethod
    def __get_word_vectors():
        if not NLProcessor.__word_vectors:
            NLProcessor.__word_vectors = api.load(NLProcessor.__word_vectors_id)
        return NLProcessor.__word_vectors
    
    @staticmethod
    def __normal_set(words):
        normal = set()
        for word in [word.lower() for word in words]:
            normal_word = ''.join([character for character in word if character not in NLProcessor.__filter_chars])
            normal.add(normal_word)
        return normal
    
    @staticmethod
    def __synonyms(word):
        syns = []
        for syn in wordnet.synsets(word): 
            for lemm in syn.lemmas(): 
                syn = lemm.name().replace('_', ' ')
                syns += [syn, syn + 's']
        return set([syn for syn in NLProcessor.__normal_set(syns) if word not in syn] + [word, word + 's'])

    @staticmethod
    def __normalize(text):
        return ' '.join([word.lower() for word in text.split(' ') if word not in NLProcessor.__get_stop_words()])

    @staticmethod
    def set_word_vectors(vectors):
        NLProcessor.__word_vectors = vectors

    @staticmethod
    def set_similarity_data(requirements, statement):
        NLProcessor.__sim_requirements = set.union(*[
            NLProcessor.__synonyms(req) for req in requirements
        ]) if requirements else None
        NLProcessor.__sim_statement = NLProcessor.__normalize(statement)
    
    @staticmethod
    def ready():
        NLProcessor.__get_stop_words()
        NLProcessor.__get_word_vectors()

    @staticmethod
    def similarity(phrase):
        if NLProcessor.__sim_requirements:
            compare_normal_set = NLProcessor.__normal_set(phrase.split(' '))
            if not (NLProcessor.__sim_requirements & compare_normal_set):
                return 0
        return 1 / NLProcessor.__get_word_vectors().wmdistance(NLProcessor.__normalize(phrase), NLProcessor.__sim_statement)
    
    @staticmethod
    def sentiment(phrase):
        return NLProcessor.__sentimentIA.polarity_scores(phrase)

