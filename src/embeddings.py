from functools import lru_cache
from sentence_transformers import SentenceTransformer

@lru_cache(maxsize=1)
def get_embedding_model():
    from src.config import EMBEDDING_MODEL

    return SentenceTransformer(
        EMBEDDING_MODEL,
        device="cpu"
    )


def create_embeddings(chunks):
    model = get_embedding_model()
    return model.encode(chunks, convert_to_tensor=False)


def create_query_embedding(query):
    model = get_embedding_model()
    return model.encode(query, convert_to_tensor=False)