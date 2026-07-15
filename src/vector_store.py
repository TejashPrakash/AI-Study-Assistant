import chromadb
import uuid

from functools import lru_cache

from src.config import DATABASE_PATH

COLLECTION_NAME = "study_notes"


@lru_cache(maxsize=1)
def get_collection():

    client = chromadb.PersistentClient(
        path=DATABASE_PATH
    )

    return client.get_or_create_collection(
        COLLECTION_NAME
    )


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


def search(query_embedding, n_results=3):

    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )

    return {
        "documents": results["documents"][0],
        "distances": results["distances"][0]
    }