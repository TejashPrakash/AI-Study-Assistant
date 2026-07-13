import chromadb
import uuid
from src.config import DATABASE_PATH

client = chromadb.PersistentClient(path=DATABASE_PATH)

COLLECTION_NAME = "study_notes"


def store_chunks(chunks, embeddings):

    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass

    collection = client.create_collection(COLLECTION_NAME)

    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )


def search(query_embedding, n_results=3):

    collection = client.get_collection(COLLECTION_NAME)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )

    return {
        "documents": results["documents"][0],
        "distances": results["distances"][0]
    }