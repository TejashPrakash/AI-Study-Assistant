import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.prompt import (
    GENERAL_CHAT_PROMPT,
    RAG_CHAT_PROMPT
)

load_dotenv()

# ==========================================
# Gemini Client
# ==========================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ==========================================
# Models
# ==========================================

CHAT_MODEL = "models/gemini-3.5-flash"

FAST_MODEL = "models/gemini-3.1-flash-lite"

ADVANCED_MODEL = "models/gemini-3.1-pro-preview"

FALLBACK_MODELS = [
    CHAT_MODEL,
    FAST_MODEL,
    "models/gemini-2.5-flash",
    "models/gemini-2.0-flash"
]


# ==========================================
# Internal Generator
# ==========================================

def _generate(
    prompt,
    models,
    temperature=0.2,
    max_tokens=2048
):
    """
    Internal Gemini generator with fallback models.
    """

    last_error = None

    for model in models:

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )

            return response.text

        except Exception as e:

            last_error = e

            error = str(e)

            if "429" in error or "503" in error:

                print(f"{model} overloaded... trying next model")

                time.sleep(1)

                continue

            print(error)

            continue

    return f"❌ All Gemini models failed.\n\n{last_error}"


# ==========================================
# Chat (General + PDF)
# ==========================================

def ask_gemini(question, context=""):
    """
    Chat with or without RAG context.
    """

    if context.strip():

        prompt = RAG_CHAT_PROMPT.format(
            context=context,
            question=question
        )

    else:

        prompt = GENERAL_CHAT_PROMPT.format(
            question=question
        )

    return _generate(
        prompt=prompt,
        models=[
            CHAT_MODEL,
            FAST_MODEL
        ],
        temperature=0.4,
        max_tokens=2048
    )


# ==========================================
# Generic Prompt
# ==========================================

def ask_gemini_prompt(
    prompt,
    fast=False,
    advanced=False,
    temperature=0.2,
    max_tokens=2048
):
    """
    Generic Gemini prompt.

    Parameters
    ----------
    fast : bool
        Uses Flash Lite

    advanced : bool
        Uses Gemini Pro

    temperature : float
        Creativity

    max_tokens : int
        Maximum output tokens
    """

    if advanced:

        models = [
            ADVANCED_MODEL,
            CHAT_MODEL
        ]

    elif fast:

        models = [
            FAST_MODEL,
            CHAT_MODEL
        ]

    else:

        models = FALLBACK_MODELS

    return _generate(
        prompt=prompt,
        models=models,
        temperature=temperature,
        max_tokens=max_tokens
    )