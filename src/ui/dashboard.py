import streamlit as st


def render_dashboard():

    st.title("📚 AI Study Assistant")

    st.subheader("Your AI-powered Study Companion")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.info("""
### 💬 Chat with AI

Ask questions naturally or chat with your uploaded PDF.
""")

        st.success("""
### 📝 Generate Notes

Create structured notes from any chapter.
""")

    with col2:

        st.warning("""
### 🧠 Flashcards

Revise quickly with AI-generated flashcards.
""")

        st.error("""
### ❓ Quiz Generator

Practice MCQs generated from your study material.
""")

    st.markdown("---")

    st.subheader("🚀 How to use")

    st.markdown("""
1. 📄 Upload a PDF using the sidebar.
2. 💬 Chat with your document.
3. 📝 Generate Notes.
4. 🧠 Revise with Flashcards.
5. ❓ Test yourself using Quizzes.
""")