import os
from dotenv import load_dotenv; load_dotenv()
import mysql.connector

class Database:
    __insertion = 'insert into summaries (source, summary, topic) values (%s, %s, %s)'
    __db = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE'))
    __cursor = __db.cursor()

    @staticmethod
    def add_values(vals):
        if type(vals) is list:
            Database.__cursor.executemany(Database.__insertion, vals)
        else:
            Database.__cursor.execute(Database.__insertion, vals)
        Database.__db.commit()

