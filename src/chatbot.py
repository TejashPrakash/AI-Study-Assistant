import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


MODELS = [
    "gemini-3.5-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash"
]


def ask_gemini(question, context=""):

    prompt = f"""
You are an AI Study Assistant.

Use ONLY the provided study material.

Do NOT use outside knowledge.

If the answer is not found in the study material, reply exactly:

"I could not find that information in the uploaded PDF."

Study Material:
{context}

Question:
{question}
"""

    last_error = None

    for model_name in MODELS:

        try:

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            return response.text

        except Exception as e:

            last_error = e

            error_text = str(e)

            # Retry only temporary errors
            if "503" in error_text or "429" in error_text:

                print(f"{model_name} overloaded. Trying next model...")

                time.sleep(1)

                continue

            # Permanent error
            return f"❌ {e}"

    return f"❌ All Gemini models failed.\n\n{last_error}"