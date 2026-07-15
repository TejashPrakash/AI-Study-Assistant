from src.chatbot import ask_gemini
from src.prompt import NOTES_PROMPT
from src.retriever import retrieve_context


def generate_notes():

    question = "Generate complete study notes from this chapter."

    context, documents, distances, found = retrieve_context(
        question,
        top_k=10
    )

    if not found:
        return "No study material found."

    prompt = NOTES_PROMPT.format(
        context=context
    )

    notes = ask_gemini(
        question=prompt,
        context=context
    )

    return notes