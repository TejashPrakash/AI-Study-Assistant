import os
import time
from dotenv import load_dotenv
from google import genai

from src.prompt import (
    GENERAL_CHAT_PROMPT,
    RAG_CHAT_PROMPT
)

from src.config import GEMINI_MODELS

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ===============================
# General Chat / PDF Chat
# ===============================

def ask_gemini(question, context=""):

    if context.strip():

        prompt = RAG_CHAT_PROMPT.format(
            context=context,
            question=question
        )

    else:

        prompt = GENERAL_CHAT_PROMPT.format(
            question=question
        )

    return ask_gemini_prompt(prompt)


# ===============================
# Generic Prompt
# ===============================

def ask_gemini_prompt(prompt):

    last_error = None

    for model_name in GEMINI_MODELS:

        try:

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            return response.text

        except Exception as e:

            last_error = e

            error_text = str(e)

            if "503" in error_text or "429" in error_text:

                print(f"{model_name} overloaded. Trying next model...")

                time.sleep(1)

                continue

            return f"❌ {e}"

    return f"❌ All Gemini models failed.\n\n{last_error}"