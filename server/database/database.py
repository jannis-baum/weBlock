from pymongo import MongoClient


class Database:
    __client = MongoClient("mongodb://localhost:27017/")
    __db = __client["weblock"]
    __table = __db["summaries"]

    @staticmethod
    def insert(vals):
        summary = {"source": vals[0], "text": vals[1], "topic": vals[2]}
        Database.__table.insert_one(summary)

    @staticmethod
    def get_summaries():
        return [(element["text"], element["topic"]) for element in Database.__table.find({}, {"text": 1})]

    @staticmethod
    def get_topics():
        return list(set([element["topic"] for element in Database.__table.find({}, {"text": 1})]))

class DatabasePositive:
    __client = MongoClient("mongodb://localhost:27017/")
    __db = __client["weblock"]
    __table = __db["positive_sentences"]

    @staticmethod
    def insert(value):
        row = {"paragraph": value}
        DatabasePositive.__table.insert_one(row)

    @staticmethod
    def get_sentences():
        return [
            element["paragraph"]
        for element in DatabasePositive.__table.find({}, {"paragraph": 1})]

