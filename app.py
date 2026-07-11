import streamlit as st
from src.chatbot import ask_gemini

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Study Assistant")

question = st.text_input("Ask me anything")

if st.button("Ask AI"):
    if question:
        with st.spinner("Thinking..."):
            answer = ask_gemini(question)
            st.success(answer)