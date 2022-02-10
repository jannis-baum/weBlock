from websockets import Data
import yaml

class Database:
    __mock_database_name = '.mock-database.yaml'

    @staticmethod
    def __get_data():
        try:
            with open(Database.__mock_database_name, 'r') as mock_db:
                return yaml.safe_load(mock_db.read())
        except:
            return list()

    @staticmethod
    def insert(vals):
        data = Database.__get_data()
        data.append(dict(zip(['source', 'text', 'topic'], vals)))
        with open(Data.__mock_database_name, 'w') as mock_db:
            mock_db.write(yaml.safe_dump(data))
    
    @staticmethod
    def get_summaries():
        return [row['text'] for row in Database.__get_data()]

