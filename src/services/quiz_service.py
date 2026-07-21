from src.chatbot import ask_gemini_prompt
from src.prompt import QUIZ_PROMPT
from src.utils.quiz_parser import parse_quiz
from src.utils.ai_cache import (
    load_cache,
    save_cache
)


# =====================================
# Generate Quiz
# =====================================

def generate_quiz(
    pdf_text,
    difficulty="Medium",
    num_questions=10
):
    """
    Generate AI quiz from PDF.
    Uses cache for instant regeneration.
    """

    # -------------------------------
    # Cache Key
    # -------------------------------

    cache_key = (
        f"quiz_{difficulty}_{num_questions}"
    )

    cached = load_cache(
        cache_key,
        pdf_text
    )

    if cached:
        return cached

    # -------------------------------
    # Prompt
    # -------------------------------

    prompt = QUIZ_PROMPT.format(
        context=pdf_text,
        difficulty=difficulty,
        num_questions=num_questions
    )

    # -------------------------------
    # Gemini
    # -------------------------------

    response = ask_gemini_prompt(
        prompt,
        fast=True,
        temperature=0.1
    )

    # -------------------------------
    # Clean Markdown Fences
    # -------------------------------

    response = response.strip()

    if response.startswith("```json"):
        response = response[7:]

    if response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    # -------------------------------
    # Parse
    # -------------------------------

    try:

        quiz = parse_quiz(
            response
        )

    except Exception:

        quiz = []

    # -------------------------------
    # Save Cache
    # -------------------------------

    save_cache(
        cache_key,
        pdf_text,
        quiz
    )

    return quiz