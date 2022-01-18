import os
from dotenv import load_dotenv; load_dotenv()
import mysql.connector

class Database:
    __db = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE'))
    __cursor = __db.cursor()

    @staticmethod
    def execute(sql):
        Database.__cursor.execute(sql)
        Database.__db.commit()

