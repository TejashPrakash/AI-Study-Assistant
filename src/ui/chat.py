import streamlit as st

from src.chatbot import ask_gemini
from src.services.chat_service import generate_chat_response


def render_chat(uploaded_file, pdf_text):

    st.title("💬 AI Chat")

    if not uploaded_file:

        st.title("📚 AI Study Assistant")
        st.caption("Your AI-powered learning companion")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:

            st.info("""
### 💬 AI Chat
Ask questions naturally or chat with your uploaded PDF.
""")

            st.success("""
### 📝 Notes
Generate structured study notes in seconds.
""")

        with col2:

            st.warning("""
### 🧠 Flashcards
Create AI-generated flashcards for quick revision.
""")

            st.error("""
### ❓ Quiz
Test yourself with automatically generated MCQs.
""")

        st.markdown("---")

        st.subheader("🚀 Getting Started")

        st.markdown("""
1. 📄 Upload your PDF from the sidebar.
2. 💬 Chat with your study material.
3. 📝 Generate notes.
4. 🧠 Revise with flashcards.
5. ❓ Practice quizzes.
""")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask about your PDF..."
        if uploaded_file
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

            if not uploaded_file:

                with st.spinner("🤖 Thinking..."):

                    answer = ask_gemini(prompt)

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

                    c1, c2, c3 = st.columns(3)

                    c1.metric(
                        "Retrieval",
                        f"{performance['retrieval']} s"
                    )

                    c2.metric(
                        "Gemini",
                        f"{performance['gemini']} s"
                    )

                    c3.metric(
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