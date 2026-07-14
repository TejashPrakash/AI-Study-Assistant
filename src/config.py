import os

# ===========================
# Base Paths
# ===========================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASE_PATH = os.path.join(BASE_DIR, "database")

DATA_PATH = os.path.join(BASE_DIR, "data")

UPLOADS_PATH = os.path.join(DATA_PATH, "uploads")

CACHE_PATH = os.path.join(DATA_PATH, "cache")

GENERATED_PATH = os.path.join(DATA_PATH, "generated")

# ===========================
# Embedding Settings
# ===========================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

TOP_K = 3

SIMILARITY_THRESHOLD = 1.2

# ===========================
# Gemini Models
# ===========================

GEMINI_MODELS = [

    "gemini-3.5-flash",

    "gemini-2.5-flash",

    "gemini-2.0-flash"

]