from os import fpathconf
import gensim.downloader as api
import nltk
nltk.download('wordnet'); nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')
from nltk.corpus import wordnet
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

class NLProcessor:
    __filter_chars = ['.', ',', '?', ';', '"', '#', '\'', '!', '‘', '’', '“', '”', '…', ':', '_', '*'] 
    __stop_words = None
    __word_vectors_id = 'word2vec-google-news-300'
    __word_vectors = None
    __sim_requirements = None
    __sim_statements = list()
    __sentimentIA = SentimentIntensityAnalyzer()

    @staticmethod
    def __get_stop_words():
        if not NLProcessor.__stop_words:
            NLProcessor.__stop_words = set(stopwords.words('english'))
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
    def set_similarity_data(requirements, sim_statements):
        NLProcessor.__sim_requirements = set.union(*[
            NLProcessor.__synonyms(req) for req in requirements
        ]) if requirements else None
        NLProcessor.__sim_statements = sim_statements

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
        return 1 / (sum([NLProcessor.__get_word_vectors().wmdistance(NLProcessor.__normalize(phrase), sim) for sim in NLProcessor.__sim_statements]) / len(NLProcessor.__sim_statements))
    
    @staticmethod
    def sentiment(phrase):
        return NLProcessor.__sentimentIA.polarity_scores(phrase)

    @staticmethod
    def summarize(document):
        if not document: return []
        sentences = sent_tokenize(document)
        tokens = list({ token for sentence in sentences for token in word_tokenize(sentence) if token not in NLProcessor.__get_stop_words() })

        word_frequencies = [ (token, document.count(token)) for token in tokens ]
        word_frequencies.sort(key=lambda x: x[1])
        max_frequency = word_frequencies[-1][1]

        weighted_frequencies = { freq[0]: freq[1] / max_frequency for freq in word_frequencies }

        sentence_scores = [
            (sentence, sum([ weighted_frequencies[word] for word in sentence.split(' ') if word in tokens ]))
        for sentence in sentences]
        sentence_scores.sort(reverse=True, key=lambda x: x[1])
        return [(NLProcessor.__normalize(sentence)) for sentence, _ in sentence_scores[:max(2, int(len(sentences) / 20))]]
    
