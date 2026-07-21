import time

from src.retriever import retrieve_context
from src.chatbot import ask_gemini

# -----------------------
# Simple Memory Cache
# -----------------------

CHAT_CACHE = {}


def generate_chat_response(question):

    total_start = time.perf_counter()

    # -----------------------
    # Return cached response
    # -----------------------

    if question in CHAT_CACHE:

        cached = CHAT_CACHE[question]

        cached["performance"] = {
            "retrieval": 0,
            "gemini": 0,
            "total": 0
        }

        return (
            cached["answer"],
            cached["documents"],
            cached["distances"],
            cached["found"],
            cached["performance"]
        )

    # -----------------------
    # Retrieval
    # -----------------------

    retrieval_start = time.perf_counter()

    context, documents, distances, found = retrieve_context(question)

    retrieval_time = round(
        time.perf_counter() - retrieval_start,
        3
    )

    # -----------------------
    # Gemini
    # -----------------------

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

    CHAT_CACHE[question] = {
        "answer": answer,
        "documents": documents,
        "distances": distances,
        "found": found,
        "performance": performance
    }

    return (
        answer,
        documents,
        distances,
        found,
        performance
    )