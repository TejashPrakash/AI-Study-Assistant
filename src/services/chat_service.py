import time

from src.retriever import retrieve_context
from src.chatbot import ask_gemini


def generate_chat_response(question):
    """
    Generate a response using RAG.

    Returns:
        answer,
        documents,
        distances,
        found,
        performance
    """

    total_start = time.perf_counter()

    # ------------------------
    # Retrieval
    # ------------------------

    retrieval_start = time.perf_counter()

    context, documents, distances, found = retrieve_context(question)

    retrieval_time = round(
        time.perf_counter() - retrieval_start,
        3
    )

    # ------------------------
    # Gemini
    # ------------------------

    gemini_time = 0

    if found:

        gemini_start = time.perf_counter()

        answer = ask_gemini(
            question,
            context
        )

        gemini_time = round(
            time.perf_counter() - gemini_start,
            3
        )

    else:

        answer = "❌ I could not find that information in the uploaded PDF."

    total_time = round(
        time.perf_counter() - total_start,
        3
    )

    performance = {
        "retrieval": retrieval_time,
        "gemini": gemini_time,
        "total": total_time
    }

    return (
        answer,
        documents,
        distances,
        found,
        performance
    )