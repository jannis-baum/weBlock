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
        return [(row["text"], row["topic"]) for row in Database.__get_data()]

    @staticmethod
    def get_topics():
        return list(set([row["topic"] for row in Database.__get_data()]))

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
            return {
                "paragraphs": list(),
                "vectors": list()
            }

    @staticmethod
    def __write_data(data):
        with open(DatabasePositive.__mock_database_name, "w") as mock_db:
            yaml.dump(data, mock_db, default_flow_style=False)
        
    @staticmethod
    def insert_paragraph(paragraph):
        data = DatabasePositive.__get_data()
        data["paragraphs"].append(paragraph)
        DatabasePositive.__write_data(data)

    @staticmethod
    def insert_vector(vector):
        data = DatabasePositive.__get_data()
        data["vectors"].append(vector)
        DatabasePositive.__write_data(data)

    @staticmethod
    def get_topic_matrix():
        return [vector for vector in DatabasePositive.__get_data()["vectors"]]

    @staticmethod
    def get_sentences():
        return [paragraph for paragraph in DatabasePositive.__get_data()["paragraphs"]]

    def get_sentence(idx):
        return DatabasePositive.__get_data()["paragraphs"][idx]

