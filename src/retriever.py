from src.embeddings import create_query_embedding
from src.vector_store import search
from src.config import SIMILARITY_THRESHOLD


def retrieve_context(question, top_k=3):
    """
    Retrieves the most relevant context from ChromaDB.

    Args:
        question (str): User query.
        top_k (int): Number of chunks to retrieve.

    Returns:
        context (str)
        documents (list)
        distances (list)
        found (bool)
    """

    query_embedding = create_query_embedding(question)

    results = search(
        query_embedding=query_embedding,
        n_results=top_k
    )

    documents = results["documents"]
    distances = results["distances"]

    if not documents:
        return "", [], [], False

    best_distance = distances[0]

    if best_distance > SIMILARITY_THRESHOLD:
        return "", documents, distances, False

    context = "\n\n".join(documents)

    return context, documents, distances, True