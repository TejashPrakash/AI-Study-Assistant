from functools import lru_cache
from sentence_transformers import SentenceTransformer

@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    model = get_embedding_model()
    return model.encode(chunks, convert_to_tensor=False)


def create_query_embedding(query):
    model = get_embedding_model()
    return model.encode(query, convert_to_tensor=False)