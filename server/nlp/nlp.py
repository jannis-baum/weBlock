import gensim.downloader as api

from nltk.corpus import wordnet
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re


class NLProcessor:
    __stopwords = set(stopwords.words('english'))
    __ps = PorterStemmer()
    __word_vectors_id = 'word2vec-google-news-300'
    __word_vectors = None
    __sim_requirements = None
    __sim_statements = list()
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
                NLProcessor.__get_word_vectors().wmdistance(NLProcessor.__normal_tokens(doc), summary)
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

        sentences = sent_tokenize(doc)
        tokens = list(
            {
                token
                for sentence in sentences
                for token in word_tokenize(sentence)
                if token not in NLProcessor.__stopwords
            }
        )

        word_frequencies = [(token, doc.count(token)) for token in tokens]
        word_frequencies.sort(key=lambda x: x[1])
        max_frequency = word_frequencies[-1][1]

        weighted_frequencies = {
            freq[0]: freq[1] / max_frequency for freq in word_frequencies
        }

        sentence_scores = [
            (
                sentence,
                sum(
                    [
                        weighted_frequencies[word]
                        for word in sentence.split(" ")
                        if word in tokens
                    ]
                ),
            )
            for sentence in sentences
        ]
        sentence_scores.sort(reverse=True, key=lambda x: x[1])
        return ''.join([
            (NLProcessor.normalize(sentence))
            for sentence, _ in sentence_scores[: max(2, int(len(sentences) / 20))]
        ])

