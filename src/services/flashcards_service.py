from src.chatbot import ask_gemini_prompt
from src.prompt import FLASHCARDS_PROMPT
from src.utils.flashcard_parser import parse_flashcards
from src.utils.ai_cache import (
    load_cache,
    save_cache
)


# ======================================
# Generate Flashcards
# ======================================

def generate_flashcards(pdf_text):
    """
    Generate AI flashcards from PDF.
    Uses cache for instant regeneration.
    """

    # -------------------------------
    # Cache
    # -------------------------------

    cached = load_cache(
        "flashcards",
        pdf_text
    )

    if cached:
        return cached

    # -------------------------------
    # Prompt
    # -------------------------------

    prompt = FLASHCARDS_PROMPT.format(
        context=pdf_text
    )

    # -------------------------------
    # Gemini
    # -------------------------------

    response = ask_gemini_prompt(
        prompt,
        fast=True,
        temperature=0.2
    )

    # -------------------------------
    # Parse
    # -------------------------------

    try:

        flashcards = parse_flashcards(
            response
        )

    except Exception:

        flashcards = []

    # -------------------------------
    # Save Cache
    # -------------------------------

    save_cache(
        "flashcards",
        pdf_text,
        flashcards
    )

    return flashcards