import os
from dotenv import load_dotenv; load_dotenv()

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

SEARCH_QUERY = os.getenv('SEARCH_QUERY')

