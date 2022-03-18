from definitions import DATABASE_NEGATIVE_PATH, DATABASE_POSITIVE_PATH
import yaml


class DatabaseNegative:
    @staticmethod
    def __get_data():
        try:
            with open(DATABASE_NEGATIVE_PATH, "r") as mock_db:
                return yaml.safe_load(mock_db.read())
        except:
            return {
                'articles': dict(),
                'sources': list()
            }

    @staticmethod
    def insert(topic, summary, source):
        data = DatabaseNegative.__get_data()
        if topic in data['articles']: data['articles'][topic].append(summary)
        else: data['articles'][topic] = [summary]
        data['sources'].append(source)
        with open(DATABASE_NEGATIVE_PATH, "w") as mock_db:
            yaml.dump(data, mock_db, default_flow_style=False)

    @staticmethod
    def get_summaries_by_topics():
        return DatabaseNegative.__get_data()['articles']

    @staticmethod
    def get_sources():
        return DatabaseNegative.__get_data()['sources']

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

