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
# Configuration
# ======================================

CHUNK_SIZE = 5000
GROUP_SIZE = 10
MAX_WORKERS = 4


# ======================================
# Split Text into Chunks
# ======================================

def chunk_text(text, max_chars=CHUNK_SIZE):
    """
    Split text into manageable chunks.
    Works for PDFs of any size.
    """

    return [
        text[i:i + max_chars]
        for i in range(0, len(text), max_chars)
    ]


# ======================================
# Summarize One Chunk
# ======================================

def summarize_chunk(section):
    """
    Generate a detailed summary for one chunk.
    """

    prompt = SECTION_SUMMARY_PROMPT.format(
        context=section
    )

    try:

        return ask_gemini_prompt(
            prompt,
            fast=True,
            temperature=0.2,
            max_tokens=1000
        )

    except Exception as e:

        return f"Error summarizing section: {e}"


# ======================================
# Summarize a Group of Summaries
# ======================================

def summarize_group(summaries):
    """
    Merge a group of summaries into a higher-level summary.
    """

    combined = "".join(summaries)

    prompt = f"""
You are an expert study assistant.

Combine the following summaries into one detailed and well-organized summary.
Preserve all important concepts, formulas, reactions, examples, and exam-relevant points.

Summaries:
{combined}
"""

    return ask_gemini_prompt(
        prompt,
        fast=True,
        temperature=0.2,
        max_tokens=1500
    )


# ======================================
# Hierarchical Summarization
# ======================================

def hierarchical_summarize(summaries):
    """
    Recursively summarize summaries until they fit into one final prompt.
    This allows processing of N-number of pages.
    """

    while len(summaries) > GROUP_SIZE:

        grouped_summaries = [
            summaries[i:i + GROUP_SIZE]
            for i in range(0, len(summaries), GROUP_SIZE)
        ]

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

            summaries = list(
                executor.map(
                    summarize_group,
                    grouped_summaries
                )
            )

    return "".join(summaries)


# ======================================
# Generate Notes
# ======================================

def generate_notes(pdf_text):
    """
    Generate detailed study notes from a PDF of any size.
    Supports N-number of pages using hierarchical summarization.
    """

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
    # Split PDF into Chunks
    # -------------------------------

    sections = chunk_text(pdf_text)

    # -------------------------------
    # Generate Chunk Summaries in Parallel
    # -------------------------------

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        summaries = list(
            executor.map(
                summarize_chunk,
                sections
            )
        )

    # -------------------------------
    # Hierarchical Summarization
    # -------------------------------

    combined_summary = hierarchical_summarize(summaries)

    # -------------------------------
    # Generate Final Detailed Notes
    # -------------------------------

    final_prompt = NOTES_PROMPT.format(
        context=combined_summary
    )

    notes = ask_gemini_prompt(
        final_prompt,
        temperature=0.3,
        max_tokens=8000
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