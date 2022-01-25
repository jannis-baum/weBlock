from nltk.tokenize import word_tokenize, sent_tokenize

class NLProcessor:
    __stop_words_path = 'stop_words_en.txt'
    __stop_words = None

    @staticmethod
    def __get_stop_words():
        if not NLProcessor.__stop_words:
            with open(NLProcessor.__stop_words_path, 'r') as fp:
                NLProcessor.__stop_words = fp.read().split('\n')
        return NLProcessor.__stop_words

    @staticmethod
    def __normalize(text):
        return ' '.join([word.lower() for word in text.split(' ') if word not in NLProcessor.__get_stop_words()])

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

