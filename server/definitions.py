import os
from dotenv import load_dotenv

load_dotenv(".env.example")

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

SEARCH_QUERY = os.getenv("SEARCH_QUERY")
SEARCH_QUERIES = list(eval(os.getenv("SEARCH_QUERIES")))
