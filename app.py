import streamlit as st

from src.pdf_loader import extract_text_from_pdf
from src.text_splitter import split_text
from src.embeddings import create_embeddings
from src.vector_store import store_chunks
from src.services.chat_service import generate_chat_response
from src.pdf_utils import get_pdf_hash
from src.cache_manager import pdf_exists, add_pdf
from src.config import EMBEDDING_MODEL, TOP_K

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

    # Footer
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

    if not pdf_exists(pdf_hash):

        with st.spinner("📄 Processing PDF..."):

            pdf_text = extract_text_from_pdf(uploaded_file)

            chunks = split_text(pdf_text)

            embeddings = create_embeddings(chunks)

            store_chunks(chunks, embeddings)

            add_pdf(pdf_hash)

        st.sidebar.success("✅ PDF Indexed Successfully")

    else:

        st.sidebar.success("✅ PDF Already Indexed")

        pdf_text = extract_text_from_pdf(uploaded_file)

        chunks = split_text(pdf_text)

    if chunks:

        st.sidebar.markdown("---")

        st.sidebar.metric("Chunks", len(chunks))

        st.sidebar.metric("Embedding Model", EMBEDDING_MODEL)

        st.sidebar.metric("Top K", TOP_K)

# ===========================
# CHAT
# ===========================

if feature == "💬 Chat":

    st.title("💬 AI Chat")

    if not uploaded_file:

        st.info("""
### 👋 Welcome to AI Study Assistant

Upload a PDF to begin.

You can:

- 💬 Chat with your notes
- 📝 Generate Notes
- 🧠 Create Flashcards
- ❓ Generate Quiz
- 📅 Build Study Planner
        """)

    else:

        # Chat History

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat Input

        prompt = st.chat_input("Ask anything about your PDF...")

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

                with st.spinner("🔍 Searching relevant study material..."):

                    answer, documents, distances, found = generate_chat_response(prompt)

                    with st.expander("🔍 Debug Mode"):

                        if documents:

                            for i, chunk in enumerate(documents):

                                st.write(f"### Chunk {i+1}")

                                st.write(chunk[:500])

                                st.write(f"Distance: {distances[i]:.4f}")

                st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        with st.expander("📄 View Extracted Text"):

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

            with st.spinner("Generating Notes..."):

                from src.services.notes_service import generate_notes

                st.session_state.notes = generate_notes(pdf_text)

        if "notes" in st.session_state:

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