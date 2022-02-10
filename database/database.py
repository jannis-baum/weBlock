import os
from dotenv import load_dotenv; load_dotenv()
from pymongo import MongoClient

class Database:
    __client = MongoClient("mongodb://localhost:27017/")
    __db = __client["weblock"]
    __table = __db["summaries"]

    @staticmethod
    def insert(vals):
        summary = {
            'source' : vals[0],
            'text' : vals[1],
            'topic' : vals[2]
        }
        Database.__table.insert_one(summary)

    def get_summaries():
        return [element['text'] for element in Database.__table.find({},{'text': 1 })]

