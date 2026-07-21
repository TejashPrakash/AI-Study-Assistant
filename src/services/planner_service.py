import json

from src.chatbot import ask_gemini_prompt
from src.prompt import PLANNER_PROMPT
from src.utils.ai_cache import (
    load_cache,
    save_cache
)


# =====================================
# Generate Planner
# =====================================

def generate_planner(
    pdf_text,
    days=7,
    hours_per_day=2
):
    """
    Generate AI study planner from PDF.
    Uses cache for instant regeneration.
    """

    # -------------------------------
    # Cache Key
    # -------------------------------

    cache_key = (
        f"planner_{days}_{hours_per_day}"
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

    prompt = PLANNER_PROMPT.format(
        context=pdf_text,
        days=days,
        hours_per_day=hours_per_day
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
    # Clean Markdown Fences
    # -------------------------------

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    # -------------------------------
    # Parse JSON
    # -------------------------------

    try:

        planner = json.loads(
            response
        )

    except Exception:

        planner = []

    # -------------------------------
    # Save Cache
    # -------------------------------

    save_cache(
        cache_key,
        pdf_text,
        planner
    )

    return planner