from src.chatbot import ask_gemini
from src.prompt import NOTES_PROMPT


def generate_notes(text):

    prompt = NOTES_PROMPT.format(
        text=text
    )

    notes = ask_gemini(
        question=prompt,
        context=text
    )

    return notes