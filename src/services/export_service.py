from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]

body_style = styles["BodyText"]


# ==========================================
# Generic PDF Creator
# ==========================================

def create_pdf(title, sections, filename):

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph(title, title_style)
    )

    story.append(
        Spacer(1, 20)
    )

    for heading, content in sections:

        story.append(
            Paragraph(heading, heading_style)
        )

        story.append(
            Paragraph(
                str(content).replace("\n", "<br/>"),
                body_style
            )
        )

        story.append(
            Spacer(1, 12)
        )

    doc.build(story)

    return filename


# ==========================================
# Notes
# ==========================================

def generate_notes_pdf(notes):

    sections = [
        (
            "Study Notes",
            notes
        )
    ]

    return create_pdf(
        title="AI Study Assistant",
        sections=sections,
        filename="study_notes.pdf"
    )


# ==========================================
# Flashcards
# ==========================================

def generate_flashcards_pdf(flashcards):

    sections = []

    for i, card in enumerate(flashcards, start=1):

        content = (
            f"<b>Question:</b><br/>{card['question']}<br/><br/>"
            f"<b>Answer:</b><br/>{card['answer']}"
        )

        sections.append(
            (
                f"Flashcard {i}",
                content
            )
        )

    return create_pdf(
        title="AI Flashcards",
        sections=sections,
        filename="flashcards.pdf"
    )


# ==========================================
# Quiz
# ==========================================

def generate_quiz_pdf(quiz):

    sections = []

    for i, q in enumerate(quiz, start=1):

        options = "<br/>".join([
            f"A. {q['options'][0]}",
            f"B. {q['options'][1]}",
            f"C. {q['options'][2]}",
            f"D. {q['options'][3]}"
        ])

        content = (
            f"{q['question']}<br/><br/>"
            f"{options}<br/><br/>"
            f"<b>Correct Answer:</b> {q['answer']}<br/><br/>"
            f"<b>Explanation:</b><br/>{q['explanation']}"
        )

        sections.append(
            (
                f"Question {i}",
                content
            )
        )

    return create_pdf(
        title="AI Quiz",
        sections=sections,
        filename="quiz.pdf"
    )


# ==========================================
# Planner
# ==========================================

def generate_planner_pdf(planner):

    sections = []

    for day in planner:

        topics = "<br/>".join(
            f"• {topic}"
            for topic in day["topics"]
        )

        sections.append(
            (
                f"Day {day['day']}",
                topics
            )
        )

    return create_pdf(
        title="AI Study Planner",
        sections=sections,
        filename="study_planner.pdf"
    )