from src.chatbot import ask_gemini_prompt
from src.prompt import QUIZ_PROMPT
from src.utils.quiz_parser import parse_quiz


def generate_quiz(pdf_text, difficulty="Medium", num_questions=10):

    prompt = QUIZ_PROMPT.format(
        context=pdf_text,
        difficulty=difficulty,
        num_questions=num_questions
    )

    response = ask_gemini_prompt(prompt)

    # Remove accidental markdown fences if Gemini adds them
    response = response.strip()

    if response.startswith("```json"):
        response = response[7:]

    if response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    quiz = parse_quiz(response)

    return quiz