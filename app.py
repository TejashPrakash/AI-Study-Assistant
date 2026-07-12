import streamlit as st
from src.chatbot import ask_gemini

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

# ------------ Chat History ------------ #

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💬 AI Chat")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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