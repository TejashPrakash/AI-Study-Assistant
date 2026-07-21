from src.embeddings import create_query_embedding
from src.vector_store import search
from src.config import SIMILARITY_THRESHOLD


def retrieve_context(question, top_k=5):

    query_embedding = create_query_embedding(question)

    results = search(
        query_embedding=query_embedding,
        n_results=top_k
    )

    documents = results["documents"]
    distances = results["distances"]

    if not documents:
        return "", [], [], False

    # -----------------------------
    # Remove duplicate chunks
    # -----------------------------

    unique_documents = []
    unique_distances = []

    seen = set()

    for doc, dist in zip(documents, distances):

        key = doc[:300]

        if key not in seen:

            seen.add(key)

            unique_documents.append(doc)
            unique_distances.append(dist)

    documents = unique_documents
    distances = unique_distances

    best_distance = distances[0]

    if best_distance > SIMILARITY_THRESHOLD:

        return "", documents, distances, False

    # -----------------------------
    # Limit context size
    # -----------------------------

    MAX_CONTEXT = 4

    documents = documents[:MAX_CONTEXT]
    distances = distances[:MAX_CONTEXT]

    context = "\n\n".join(documents)

    return context, documents, distances, True