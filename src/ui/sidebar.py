import streamlit as st

from src.config import TOP_K


def render_sidebar():

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
        st.caption("Version 2.0")

    return uploaded_file, feature