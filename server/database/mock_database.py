from definitions import ROOT_DIR, DATABASE_NEGATIVE_PATH, DATABASE_POSITIVE_PATH
import yaml, os


class DatabaseNegative:
    @staticmethod
    def __get_data():
        try:
            with open(DATABASE_NEGATIVE_PATH, "r") as mock_db:
                return yaml.safe_load(mock_db.read())
        except:
            return list()

    @staticmethod
    def insert(vals):
        data = DatabaseNegative.__get_data()
        data.append(dict(zip(["source", "text", "topic"], vals)))
        with open(DATABASE_NEGATIVE_PATH, "w") as mock_db:
            yaml.dump(data, mock_db, default_flow_style=False)

    @staticmethod
    def get_summaries():
        return [(row["text"], row["topic"]) for row in DatabaseNegative.__get_data()]

    @staticmethod
    def get_topics():
        return list(set([row["topic"] for row in DatabaseNegative.__get_data()]))

class DatabasePositive:
    @staticmethod
    def __get_data():
        try:
            with open(DATABASE_POSITIVE_PATH, "r") as mock_db:
                return yaml.safe_load(mock_db.read())
        except:
            return {
                "paragraphs": list(),
                "vectors": list()
            }

    @staticmethod
    def __write_data(data):
        with open(DATABASE_POSITIVE_PATH, "w") as mock_db:
            yaml.dump(data, mock_db, default_flow_style=False)

    def count_paragraphs():
        return len(DatabasePositive.__get_data()["paragraphs"])
        
    @staticmethod
    def insert_paragraph(paragraph):
        data = DatabasePositive.__get_data()
        data["paragraphs"].append(paragraph)
        DatabasePositive.__write_data(data)

    @staticmethod
    def insert_vectors(vectors):
        data = DatabasePositive.__get_data()
        data["vectors"] += vectors
        DatabasePositive.__write_data(data)

    @staticmethod
    def clear_vectors():
        data = DatabasePositive.__get_data()
        data["vectors"] = list()
        DatabasePositive.__write_data(data)

    @staticmethod
    def get_topic_matrix():
        return [vector for vector in DatabasePositive.__get_data()["vectors"]]

    @staticmethod
    def get_paragraphs():
        return [paragraph for paragraph in DatabasePositive.__get_data()["paragraphs"]]

