import streamlit as st

from src.chatbot import ask_gemini
from src.pdf_loader import extract_text_from_pdf
from src.text_splitter import split_text
from src.embeddings import create_embeddings
from src.vector_store import store_chunks
from src.services.chat_service import generate_chat_response
from src.pdf_utils import get_pdf_hash
from src.cache_manager import pdf_exists, add_pdf
from src.config import TOP_K
from src.utils.performance import Timer

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
    st.caption("Version 0.1.0")

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

🚧 Flashcards

🚧 Quiz Generator

🚧 Study Planner
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

                    timer = Timer()

                    answer, documents, distances, found, performance = generate_chat_response(prompt)

                    response_time = timer.elapsed()

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

                from src.services.notes_service import generate_notes

                st.session_state.notes = generate_notes()

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

    st.title("🧠 Flashcards")

    st.info("🚧 Coming Soon")

# ===========================
# QUIZ
# ===========================

elif feature == "❓ Quiz":

    st.title("❓ Quiz Generator")

    st.info("🚧 Coming Soon")

# ===========================
# PLANNER
# ===========================

elif feature == "📅 Planner":

    st.title("📅 Study Planner")

    st.info("🚧 Coming Soon")