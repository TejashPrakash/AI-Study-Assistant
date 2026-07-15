from src.chatbot import ask_gemini
from src.prompt import FLASHCARDS_PROMPT


def generate_flashcards(text):

    prompt = FLASHCARDS_PROMPT.format(
        text=text
    )

    flashcards = ask_gemini(
        question=prompt,
        context=text
    )

    return flashcards