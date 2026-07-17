from src.chatbot import ask_gemini_prompt
from src.prompt import FLASHCARDS_PROMPT
from src.utils.flashcard_parser import parse_flashcards


def generate_flashcards(pdf_text):

    prompt = FLASHCARDS_PROMPT.format(
        context=pdf_text
    )

    response = ask_gemini_prompt(prompt)

    print("\n========== GEMINI RESPONSE ==========\n")
    print(response)
    print("\n=====================================\n")

    flashcards = parse_flashcards(response)

    print("Parsed flashcards:", len(flashcards))

    return flashcards