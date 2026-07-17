import streamlit as st

from src.chatbot import ask_gemini
from src.utils.pdf_loader import extract_text_from_pdf
from src.utils.text_splitter import split_text
from src.embeddings import create_embeddings
from src.vector_store import store_chunks
from src.services.chat_service import generate_chat_response
from src.utils.pdf_utils import get_pdf_hash
from src.utils.cache_manager import pdf_exists, add_pdf
from src.config import TOP_K
from src.utils.performance import Timer
from src.services.notes_service import generate_notes

# ===========================
# Page Config
# ===========================

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

# ===========================
# Session State
# ===========================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "notes" not in st.session_state:
    st.session_state.notes = None

if "flashcards" not in st.session_state:
            st.session_state.flashcards = []

if "current_card" not in st.session_state:
            st.session_state.current_card = 0

if "show_answer" not in st.session_state:
            st.session_state.show_answer = False

if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False

# ===========================
# Sidebar
# ===========================

with st.sidebar:

    st.title("📚 AI Study Assistant")

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "📄 Upload PDF",
        type="pdf"
    )

    st.markdown("---")

    feature = st.radio(
        "Choose Feature",
        [
            "💬 Chat",
            "📝 Notes",
            "🧠 Flashcards",
            "❓ Quiz",
            "📅 Planner"
        ]
    )

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.caption("📚 AI Study Assistant")
    st.caption("Developed by Tejash Prakash")
    st.caption("Version 1.0")

# ===========================
# PDF Processing
# ===========================

pdf_text = None
chunks = []

if uploaded_file:

    pdf_hash = get_pdf_hash(uploaded_file)

    pdf_text = extract_text_from_pdf(uploaded_file)

    if not pdf_exists(pdf_hash):

        with st.spinner("📄 Processing PDF..."):

            chunks = split_text(pdf_text)

            embeddings = create_embeddings(chunks)

            store_chunks(chunks, embeddings)

            add_pdf(pdf_hash)

        st.sidebar.success("✅ PDF Indexed Successfully")

    else:

        st.sidebar.success("⚡ PDF Already Indexed")

        chunks = split_text(pdf_text)

    st.sidebar.markdown("---")

    st.sidebar.metric("Chunks", len(chunks))
    st.sidebar.metric("Top K", TOP_K)

# ===========================
# CHAT
# ===========================

if feature == "💬 Chat":

    st.title("💬 AI Chat")

    if not uploaded_file:

        st.info("""
# 👋 Welcome to AI Study Assistant

You can start chatting with AI immediately.

Upload a PDF anytime to enable AI-powered document chat.

### Features

✅ General AI Chat

✅ Chat with PDF (RAG)

✅ AI Notes Generator

✅ Flashcards

✅ Quiz Generator

✅ Study Planner
""")

    # Chat History

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # Chat Input

    prompt = st.chat_input(
        "Ask about your PDF..." if uploaded_file
        else "Chat with AI..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.chat_message("assistant"):

            # -----------------------
            # General AI Chat
            # -----------------------

            if not uploaded_file:

                with st.spinner("🤖 Thinking..."):

                    answer = ask_gemini(prompt)

            # -----------------------
            # PDF Chat (RAG)
            # -----------------------

            else:

                with st.spinner("🔍 Searching your PDF..."):

                    answer, documents, distances, found, performance = generate_chat_response(prompt)

                with st.expander("🔍 Retrieved Chunks"):

                    if documents:

                        for i, chunk in enumerate(documents):

                            st.markdown(f"### Chunk {i+1}")

                            st.write(chunk[:500])

                            st.caption(
                                f"Distance: {distances[i]:.4f}"
                            )

                    else:

                        st.write("No relevant chunks found.")
                
                with st.expander("⚡ Performance"):

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Retrieval",
                            f"{performance['retrieval']} s"
                        )

                    with col2:
                        st.metric(
                            "Gemini",
                            f"{performance['gemini']} s"
                        )

                    with col3:
                        st.metric(
                            "Total",
                            f"{performance['total']} s"
                        )

            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    if uploaded_file:

        with st.expander("📄 PDF Preview"):

            st.text_area(
                "Extracted Text",
                pdf_text,
                height=500
            )

# ===========================
# NOTES
# ===========================

elif feature == "📝 Notes":

    st.title("📝 Notes Generator")

    if uploaded_file:

        if st.button("📝 Generate Notes"):

            with st.spinner("📝 Generating Notes..."):

                st.session_state.notes = generate_notes(pdf_text)

        if st.session_state.notes:

            st.markdown(st.session_state.notes)

            st.download_button(
                "⬇ Download Notes",
                st.session_state.notes,
                file_name="study_notes.md",
                mime="text/markdown"
            )

    else:

        st.warning("Please upload a PDF first.")

# ===========================
# FLASHCARDS
# ===========================

elif feature == "🧠 Flashcards":

    from src.services.flashcards_service import generate_flashcards

    st.title("🧠 Flashcards")

    if not uploaded_file:

        st.warning("Please upload a PDF first.")

    else:

        if st.button("🧠 Generate Flashcards"):

            with st.spinner("Generating Flashcards..."):

                st.session_state.flashcards = generate_flashcards(pdf_text)

                st.session_state.current_card = 0
                st.session_state.show_answer = False

        if st.session_state.flashcards:

            flashcards = st.session_state.flashcards

            card = flashcards[st.session_state.current_card]

            st.progress(
                (st.session_state.current_card + 1) / len(flashcards)
            )

            st.subheader(
                f"Card {st.session_state.current_card + 1} / {len(flashcards)}"
            )

            st.markdown("### ❓ Question")
            st.info(card["question"])

            if st.button("👀 Show Answer"):

                st.session_state.show_answer = True

            if st.session_state.show_answer:

                st.markdown("### ✅ Answer")
                st.success(card["answer"])

            col1, col2 = st.columns(2)

            with col1:

                if st.button("⬅ Previous"):

                    if st.session_state.current_card > 0:

                        st.session_state.current_card -= 1
                        st.session_state.show_answer = False
                        st.rerun()

            with col2:

                if st.button("Next ➡"):

                    if st.session_state.current_card < len(flashcards) - 1:

                        st.session_state.current_card += 1
                        st.session_state.show_answer = False
                        st.rerun()

# ===========================
# QUIZ
# ===========================

elif feature == "❓ Quiz":

    from src.services.quiz_service import generate_quiz

    st.title("❓ AI Quiz Generator")

    if not uploaded_file:

        st.warning("Please upload a PDF first.")

    else:

        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
            index=1
        )

        num_questions = st.selectbox(
            "Number of Questions",
            [5, 10, 15],
            index=1
        )

        if st.button("🚀 Generate Quiz"):

            with st.spinner("Generating Quiz..."):

                st.session_state.quiz = generate_quiz(
                    pdf_text,
                    difficulty=difficulty,
                    num_questions=num_questions
                )

                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_submitted = False
                st.session_state.selected_option = None
                st.session_state.quiz_finished = False

        if st.session_state.quiz and not st.session_state.quiz_finished:

            quiz = st.session_state.quiz

            question = quiz[st.session_state.quiz_index]

            st.progress(
                (st.session_state.quiz_index + 1) / len(quiz)
            )

            st.subheader(
                f"Question {st.session_state.quiz_index + 1} / {len(quiz)}"
            )

            st.markdown(question["question"])

            option = st.radio(
                "Choose an answer:",
                ["A", "B", "C", "D"],
                format_func=lambda x: f"{x}. {question['options'][ord(x)-65]}",
                key=f"quiz_option_{st.session_state.quiz_index}"
            )

            if not st.session_state.quiz_submitted:

                if st.button("✅ Submit Answer"):

                    st.session_state.selected_option = option
                    st.session_state.quiz_submitted = True

                    if option == question["answer"]:

                        st.session_state.quiz_score += 1

                    st.rerun()

            else:

                if st.session_state.selected_option == question["answer"]:

                    st.success("✅ Correct!")

                else:

                    st.error(
                        f"❌ Incorrect! Correct Answer: {question['answer']}"
                    )

                st.info(question["explanation"])

                if st.button("➡ Next Question"):

                    st.session_state.quiz_index += 1

                    st.session_state.quiz_submitted = False
                    st.session_state.selected_option = None

                    if st.session_state.quiz_index >= len(quiz):

                        st.session_state.quiz_finished = True

                    st.rerun()

        elif st.session_state.quiz_finished:

            total = len(st.session_state.quiz)

            score = st.session_state.quiz_score

            percentage = score / total * 100

            st.success("🎉 Quiz Completed!")

            col1, col2 = st.columns(2)

            with col1:

                st.metric("Score", f"{score}/{total}")

            with col2:

                st.metric("Percentage", f"{percentage:.1f}%")

            if st.button("🔄 Retry Quiz"):

                st.session_state.quiz = []
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_submitted = False
                st.session_state.selected_option = None
                st.session_state.quiz_finished = False

                st.rerun()

# ===========================
# PLANNER
# ===========================

elif feature == "📅 Planner":

    from src.services.planner_service import generate_planner

    st.title("📅 AI Study Planner")

    if not uploaded_file:

        st.warning("Please upload a PDF first.")

    else:

        if "planner" not in st.session_state:
            st.session_state.planner = None

        st.subheader("Planner Settings")

        col1, col2 = st.columns(2)

        with col1:

            days = st.selectbox(
                "Study Duration",
                [3, 5, 7, 14, 30],
                index=2
            )

        with col2:

            hours = st.slider(
                "Hours per Day",
                1,
                8,
                2
            )

        if st.button("📅 Generate Planner"):

            with st.spinner("Creating Study Plan..."):

                st.session_state.planner = generate_planner(
                    pdf_text,
                    days=days,
                    hours_per_day=hours
                )

        if st.session_state.planner:

            planner = st.session_state.planner

            markdown_plan = "# 📅 Study Plan\n\n"

            for day in planner:

                st.markdown(f"## Day {day['day']}")

                markdown_plan += f"## Day {day['day']}\n"

                for topic in day["topics"]:

                    st.markdown(f"- {topic}")

                    markdown_plan += f"- {topic}\n"

                markdown_plan += "\n"

            st.download_button(
                "⬇ Download Planner",
                markdown_plan,
                file_name="study_plan.md",
                mime="text/markdown"
            )