import numpy as np

from definitions import TOPIC_MODEL_PATH
from database.mock_database import DatabasePositive
from btm.script.infer import BTMInferrer

class TextMatcher:
    def __init__(self):
        self.__inferrer = BTMInferrer(TOPIC_MODEL_PATH)
        self.__topic_matrix = np.array(DatabasePositive.get_topic_matrix())
        self.__paragraphs = DatabasePositive.get_paragraphs()

    def find_matching(self, document):
        topic_vector = np.array(self.__inferrer.infer(document))
        idx = np.argmax(self.__topic_matrix.dot(topic_vector))
        return self.__paragraphs[idx]

