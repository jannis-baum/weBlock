import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

SEARCH_QUERY = os.getenv("SEARCH_QUERY")
POSITIVE_QUERIES = list(eval(os.getenv("POSITIVE_QUERIES")))
