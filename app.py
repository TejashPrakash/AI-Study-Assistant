import streamlit as st

from src.ui.session import initialize_session
from src.ui.sidebar import render_sidebar
from src.ui.chat import render_chat
from src.ui.notes import render_notes
from src.ui.flashcards import render_flashcards
from src.ui.quiz import render_quiz
from src.ui.planner import render_planner
from src.services.pdf_service import process_pdf

# ===========================
# Page Config
# ===========================

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

initialize_session()

# ===========================
# Sidebar
# ===========================

uploaded_file, feature = render_sidebar()

# ===========================
# PDF Processing
# ===========================

pdf_text = process_pdf(uploaded_file)

# ===========================
# CHAT
# ===========================

if feature == "💬 Chat":

    render_chat(
        uploaded_file,
        pdf_text
    )

# ===========================
# NOTES
# ===========================

elif feature == "📝 Notes":

    render_notes(
        uploaded_file,
        pdf_text
    )

# ===========================
# FLASHCARDS
# ===========================

elif feature == "🧠 Flashcards":

    render_flashcards(
        uploaded_file,
        pdf_text
    )

# ===========================
# QUIZ
# ===========================

elif feature == "❓ Quiz":

    render_quiz(
        uploaded_file,
        pdf_text
    )

# ===========================
# PLANNER
# ===========================

elif feature == "📅 Planner":

    render_planner(
        uploaded_file,
        pdf_text
    )