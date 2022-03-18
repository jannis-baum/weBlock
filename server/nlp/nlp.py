import gensim.downloader as api

from nltk.corpus import wordnet
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re, math


class NLProcessor:
    __stopwords = set(stopwords.words('english'))
    __ps = PorterStemmer()
    __word_vectors_id = 'word2vec-google-news-300'
    __word_vectors = None
    __sim_requirements = None
    __sim_topic_summaries = dict()
    __sentimentIA = SentimentIntensityAnalyzer()


    # MARK: NORMALIZATION

    # word-tokenizes document and removes all non-alphanumeric characters
    # optionally clears stopwords and stems word
    @staticmethod
    def __normal_tokens(doc, clear_stopwords=True, stem=True):
        tokens = [token for token in word_tokenize(''.join([
            char.lower() for char in doc if char.isalnum() or char.isspace()
        ])) if not clear_stopwords or token not in NLProcessor.__stopwords]

        return [NLProcessor.__ps.stem(token) for token in tokens] if stem else tokens

    @staticmethod
    def normalize(doc):
        return ' '.join(NLProcessor.__normal_tokens(doc))


    # MARK: WORD MOVER'S DISTANCE & SYNONYMS

    # setup - lazily loaded word vectors
    @staticmethod
    def __get_word_vectors():
        if not NLProcessor.__word_vectors:
            NLProcessor.__word_vectors = api.load(NLProcessor.__word_vectors_id)
        return NLProcessor.__word_vectors
    @staticmethod
    def set_word_vectors(vectors): NLProcessor.__word_vectors = vectors
    @staticmethod
    def ready(): NLProcessor.__get_word_vectors()

    # setup - similarity data
    @staticmethod
    def set_similarity_data(requirements, topic_summaries):
        NLProcessor.__sim_requirements = (
            set.union(*[NLProcessor.__synonyms(req) for req in requirements])
            if requirements else None
        )
        NLProcessor.__sim_topic_summaries = topic_summaries

    # set of normalized (stemmed & non-stopword) synonyms
    @staticmethod
    def __synonyms(word):
        syns = [lemm.name().replace('_', ' ') for syn in wordnet.synsets(word) for lemm in syn.lemmas()]
        return set(NLProcessor.__normal_tokens(' '.join(syns + [word])))
    
    # Word Mover's Distance to closest topic summaries with synonyms as requirements
    @staticmethod
    def similarity(doc):
        if len(NLProcessor.__sim_topic_summaries) == 0: return 0
        if NLProcessor.__sim_requirements:
            compare_normal_tokens = NLProcessor.__normal_tokens(doc)
            if not (NLProcessor.__sim_requirements & compare_normal_tokens):
                return 0
        topic_sims = {
            topic: 1 / sum([
                NLProcessor.__get_word_vectors().wmdistance(NLProcessor.__normal_tokens(doc, stem=False), summary)
            for summary in summaries]) * len(summaries)
        for topic, summaries in NLProcessor.__sim_topic_summaries.items()}
        return max(topic_sims.values())


    # MARK: SENTIMENT ANALYSIS

    @staticmethod
    def sentiment(doc):
        return NLProcessor.__sentimentIA.polarity_scores(doc)


    # MARK: ARTICLE PROCESSING

    # compress multiple whitespace into one space
    @staticmethod
    def preprocess_article(doc):
        return re.sub("\s+", " ", doc)

    # summarization
    @staticmethod
    def summarize(doc):
        if not doc: return ''

        sentences = [NLProcessor.__normal_tokens(sent, stem=False) for sent in sent_tokenize(doc)]
        tokens_flat = [token for sent in sentences for token in sent]
        token_freqs = [(token, tokens_flat.count(token)) for token in set(tokens_flat)]
        max_freq = max(token_freqs, key=lambda tf: tf[1])[1]

        weighted_freqs = { tf[0]: tf[1] / max_freq for tf in token_freqs }

        sentence_scores = [
            (sent, sum([weighted_freqs[token] for token in sent]))
        for sent in sentences]
        sentence_scores.sort(reverse=True, key=lambda sent_score: sent_score[1])

        return ''.join([' '.join(sent) for sent, _ in sentence_scores[: min(3, math.ceil(len(sentences) / 20))]])

