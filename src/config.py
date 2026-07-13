import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASE_PATH = os.path.join(BASE_DIR, "database")

DATA_PATH = os.path.join(BASE_DIR, "data")

UPLOADS_PATH = os.path.join(DATA_PATH, "uploads")

CACHE_PATH = os.path.join(DATA_PATH, "cache")

GENERATED_PATH = os.path.join(DATA_PATH, "generated")