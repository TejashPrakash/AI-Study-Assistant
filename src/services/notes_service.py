from src.chatbot import ask_gemini
from src.prompt import NOTES_PROMPT


def generate_notes(text):

    prompt = NOTES_PROMPT.format(
        context=text
    )

    return ask_gemini(
        question=prompt,
        context=text
    )