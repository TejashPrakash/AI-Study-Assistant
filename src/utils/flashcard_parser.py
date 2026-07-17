import re

def parse_flashcards(text):

    flashcards = []

    pattern = r"Q:\s*(.*?)\nA:\s*(.*?)(?=\nQ:|\Z)"

    matches = re.findall(
        pattern,
        text,
        re.DOTALL
    )

    for question, answer in matches:

        flashcards.append(
            {
                "question": question.strip(),
                "answer": answer.strip()
            }
        )

    return flashcards