import streamlit as st

from src.chatbot import ask_gemini
from src.pdf_loader import extract_text_from_pdf
from src.text_splitter import split_text
from src.embeddings import create_embeddings, create_query_embedding
from src.vector_store import store_chunks, search
from src.pdf_utils import get_pdf_hash
from src.cache_manager import pdf_exists, add_pdf

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

# ---------------- Sidebar ---------------- #

with st.sidebar:

    st.title("📚 AI Study Assistant")

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.info("""
**Features**

✅ AI Chat

✅ PDF Chat (RAG)

🚧 Quiz Generator

🚧 Flashcards

🚧 Notes Generator
""")

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type="pdf"
    )

# ---------------- Chat History ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💬 AI Chat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

pdf_text = None
chunks = []

# ---------------- PDF Processing ---------------- #

if uploaded_file:

    pdf_hash = get_pdf_hash(uploaded_file)

    if not pdf_exists(pdf_hash):

        with st.spinner("Processing PDF for the first time..."):

            pdf_text = extract_text_from_pdf(uploaded_file)

            chunks = split_text(pdf_text)

            embeddings = create_embeddings(chunks)

            store_chunks(chunks, embeddings)

            add_pdf(pdf_hash)

            st.success("PDF Indexed Successfully!")

    else:

        st.success("✅ PDF already indexed.")

        pdf_text = extract_text_from_pdf(uploaded_file)

        chunks = split_text(pdf_text)

# ---------------- Chat ---------------- #

prompt = st.chat_input("Ask anything...")

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

        with st.spinner("Thinking..."):

            query_embedding = create_query_embedding(prompt)

            results = search(query_embedding)

            documents = results["documents"]
            distances = results["distances"]

            # Debug

            with st.expander("Retrieved Chunks"):

                for i, chunk in enumerate(documents):

                    st.write(f"### Chunk {i+1}")

                    st.write(chunk[:500])

                    st.write(f"Distance : {distances[i]}")

            # Lower distance = better match

            BEST_DISTANCE = distances[0]

            if BEST_DISTANCE > 1.2:

                answer = "❌ I could not find that information in the uploaded PDF."

            else:

                context = "\n\n".join(documents)

                answer = ask_gemini(prompt, context)

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# ---------------- PDF Preview ---------------- #

if pdf_text:

    with st.expander("View Extracted Text"):

        st.text_area(
            "Extracted Text",
            pdf_text,
            height=500
        )