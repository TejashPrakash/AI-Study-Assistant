from concurrent.futures import ThreadPoolExecutor

from src.chatbot import ask_gemini_prompt
from src.prompt import (
    SECTION_SUMMARY_PROMPT,
    NOTES_PROMPT
)
from src.utils.ai_cache import (
    load_cache,
    save_cache
)


# ======================================
# Chunk Text
# ======================================

def chunk_text(text, max_chars=7000):

    return [
        text[i:i + max_chars]
        for i in range(0, len(text), max_chars)
    ]


# ======================================
# Summarize One Chunk
# ======================================

def summarize_chunk(section):

    prompt = SECTION_SUMMARY_PROMPT.format(
        context=section
    )

    try:

        return ask_gemini_prompt(
            prompt,
            fast=True
        )

    except Exception as e:

        return f"Error summarizing section: {e}"

# ======================================
# Generate Notes
# ======================================

def generate_notes(pdf_text):

    # -------------------------------
    # Cache
    # -------------------------------

    cached = load_cache(
        "notes",
        pdf_text
    )

    if cached:
        return cached

    # -------------------------------
    # Split PDF
    # -------------------------------

    sections = chunk_text(pdf_text)

    # -------------------------------
    # Parallel Summarization
    # -------------------------------

    with ThreadPoolExecutor(max_workers=4) as executor:

        summaries = list(
            executor.map(
                summarize_chunk,
                sections
            )
        )

    # -------------------------------
    # Merge
    # -------------------------------

    combined_summary = "\n\n".join(summaries)

    final_prompt = NOTES_PROMPT.format(
        context=combined_summary
    )

    notes = ask_gemini_prompt(
        final_prompt, temperature=0.3
    )

    # -------------------------------
    # Save Cache
    # -------------------------------

    save_cache(
        "notes",
        pdf_text,
        notes
    )

    return notes