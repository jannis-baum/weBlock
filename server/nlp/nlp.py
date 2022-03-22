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
    __sim_summary_clusters = dict()
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

    # normalize document
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

    @staticmethod
    #set the clustered negative summarizations
    def set_similarity_clusters(requirements, summary_clusters):
        NLProcessor.__sim_requirements = (
            set.union(*[NLProcessor.__synonyms(req) for req in requirements])
            if requirements else None
        )
        NLProcessor.__sim_summary_clusters = summary_clusters

    # set of normalized (stemmed & non-stopword) synonyms
    @staticmethod
    def __synonyms(word):
        syns = [lemm.name().replace('_', ' ') for syn in wordnet.synsets(word) for lemm in syn.lemmas()]
        return set(NLProcessor.__normal_tokens(' '.join(syns + [word])))

    @staticmethod
    def cluster_similarity(doc):
        #find the cluster-key that is most similar to the doc
        best_similarity = NLProcessor.__get_word_vectors().wmdistance(NLProcessor.__normal_tokens(doc, stem=False), list(NLProcessor.__sim_summary_clusters.keys())[0])
        best_key = list(NLProcessor.__sim_summary_clusters.keys())[0]
        for cluster_key in list(NLProcessor.__sim_summary_clusters.keys()):
            current_similarity = NLProcessor.__get_word_vectors().wmdistance(NLProcessor.__normal_tokens(doc, stem=False), cluster_key)
            if current_similarity < best_similarity:
                best_key = cluster_key
                best_similarity = current_similarity
        #return the average similarity between doc and all summaries from the previously found cluster
        return sum([
            NLProcessor.__get_word_vectors().wmdistance(NLProcessor.__normal_tokens(doc, stem=False), summary)
            for summary in NLProcessor.__sim_summary_clusters[best_key]]
            ) / len(NLProcessor.__sim_summary_clusters[best_key])

    @staticmethod
    def pairdistance(doc1, doc2):
        #a public wrapper for the word movers distance needed in scrape-negative
        return NLProcessor.__get_word_vectors().wmdistance(NLProcessor.__normal_tokens(doc1, stem=False), NLProcessor.__normal_tokens(doc2, stem=False))

    # MARK: SENTIMENT ANALYSIS

    @staticmethod
    def sentiment(doc):
        return NLProcessor.__sentimentIA.polarity_scores(doc)


    # MARK: ARTICLE PROCESSING

    # compress multiple whitespace into one space
    @staticmethod
    def preprocess_article(doc):
        paragraph = re.sub("\s+", " ", doc)
        if any(c in paragraph.lower() for c in ["/", "\n","_","|", "\\", "@", "copyright"]) or len(paragraph) < 10:
            return None
        return paragraph

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

