from definitions import ROOT_DIR
import yaml, os


class Database:
    __mock_database_name = os.path.join(ROOT_DIR, "database/.mock-database.yaml")

    @staticmethod
    def __get_data():
        try:
            with open(Database.__mock_database_name, "r") as mock_db:
                return yaml.safe_load(mock_db.read())
        except:
            return list()

    @staticmethod
    def insert(vals):
        data = Database.__get_data()
        data.append(dict(zip(["source", "text", "topic"], vals)))
        with open(Database.__mock_database_name, "w") as mock_db:
            yaml.dump(data, mock_db, default_flow_style=False)

    @staticmethod
    def get_summaries():
        return [row["text"] for row in Database.__get_data()]


class DatabasePositive:
    __mock_database_name = os.path.join(
        ROOT_DIR, "database/.mock-database-positive.yaml"
    )

    @staticmethod
    def __get_data():
        try:
            with open(DatabasePositive.__mock_database_name, "r") as mock_db:
                return yaml.safe_load(mock_db.read())
        except:
            return list()

    @staticmethod
    def insert(value):
        data = DatabasePositive.__get_data()
        data.append(dict(zip(["paragraph"], value)))
        with open(DatabasePositive.__mock_database_name, "w") as mock_db:
            yaml.dump(data, mock_db, default_flow_style=False)

    @staticmethod
    def get_sentences():
        return [row["paragraph"] for row in DatabasePositive.__get_data()]
