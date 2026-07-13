import chromadb
import uuid

client = chromadb.PersistentClient(path="./database")

collection = client.get_or_create_collection(
    name="study_notes"
)


def store_chunks(chunks, embeddings):
    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )


def search(query_embedding, n_results=3):
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )

    return results["documents"][0]