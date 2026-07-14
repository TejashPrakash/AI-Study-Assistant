from src.retriever import retrieve_context
from src.chatbot import ask_gemini


def generate_chat_response(question):
    """
    Generate a response using RAG.
    Returns:
        answer,
        retrieved documents,
        distances,
        found
    """

    context, documents, distances, found = retrieve_context(question)

    if found:
        answer = ask_gemini(question, context)
    else:
        answer = "❌ I could not find that information in the uploaded PDF."

    return answer, documents, distances, found