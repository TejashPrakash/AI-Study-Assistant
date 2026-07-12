import streamlit as st
from src.chatbot import ask_gemini
from src.pdf_loader import extract_text_from_pdf

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

    st.info(
        """
        **Features**

        ✅ AI Chat

        🚧 PDF Chat

        🚧 Quiz Generator

        🚧 Flashcards

        🚧 Notes Generator
        """
    )
    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type="pdf"
    )

# ------------ Chat History ------------ #

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💬 AI Chat")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

pdf_text = None

if uploaded_file:
    with st.spinner("Reading PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)

    if pdf_text:
        st.success("PDF loaded successfully!")
    else:
        st.warning("No readable text found in the PDF.")


# Chat Input
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

            answer = ask_gemini(prompt)

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

if pdf_text:

    with st.expander("View Extracted Text"):

        st.text_area(
            "Extracted Text",
            pdf_text,
            height=500
        )