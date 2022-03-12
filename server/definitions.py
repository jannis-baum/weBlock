import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
TEMP_DIR = os.path.join(ROOT_DIR, '.temp')
os.makedirs(TEMP_DIR, exist_ok=True)

DATABASE_POSITIVE_PATH = os.path.join(ROOT_DIR, 'database', '.mock-positive.yaml')
DATABASE_NEGATIVE_PATH = os.path.join(ROOT_DIR, 'database', '.mock-negative.yaml')

SEARCH_QUERY = os.getenv("SEARCH_QUERY")
POSITIVE_QUERIES = os.getenv("POSITIVE_QUERIES").split(", ")
NEGATIVE_QUERIES = os.getenv("NEGATIVE_QUERIES").split(", ")

TRAINING_TOPICS = int(os.getenv("TRAINING_TOPICS", "20"))
TRAINING_ALPHA = float(os.getenv("TRAINING_ALPHA", "2.5"))
TRAINING_BETA = float(os.getenv("TRAINING_BETA", "0.05"))
TRAINING_ITERATIONS = int(os.getenv("TRAINING_ITERATIONS", "10"))
TRAINING_SAVE_STEPS= int(os.getenv("TRAINING_SAVE_STEPS", "500"))

TOPIC_MODEL_PATH = os.path.join(ROOT_DIR, '.btm_model')

