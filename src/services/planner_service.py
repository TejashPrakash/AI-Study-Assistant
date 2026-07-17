import json

from src.chatbot import ask_gemini_prompt
from src.prompt import PLANNER_PROMPT


def generate_planner(pdf_text, days=7, hours_per_day=2):

    prompt = PLANNER_PROMPT.format(
        context=pdf_text,
        days=days,
        hours_per_day=hours_per_day
    )

    response = ask_gemini_prompt(prompt)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    planner = json.loads(response)

    return planner