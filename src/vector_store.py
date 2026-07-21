import uuid
from functools import lru_cache

import chromadb

from src.config import DATABASE_PATH

COLLECTION_NAME = "study_notes"


# ===========================
# Cached Collection
# ===========================

@lru_cache(maxsize=1)
def get_collection():

    client = chromadb.PersistentClient(
        path=DATABASE_PATH
    )

    return client.get_or_create_collection(
        name=COLLECTION_NAME
    )


# ===========================
# Store Chunks
# ===========================

def store_chunks(chunks, embeddings):

    collection = get_collection()

    ids = [
        str(uuid.uuid4())
        for _ in chunks
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )


# ===========================
# Search
# ===========================

def search(query_embedding, n_results=5):

    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results,
        include=[
            "documents",
            "distances"
        ]
    )

    return {
        "documents": results["documents"][0],
        "distances": results["distances"][0]
    }