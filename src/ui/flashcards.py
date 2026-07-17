import streamlit as st

from src.services.flashcards_service import generate_flashcards


def render_flashcards(uploaded_file, pdf_text):

    st.title("🧠 Flashcards")

    if not uploaded_file:

        st.warning("Please upload a PDF first.")

        return

    if st.button("🧠 Generate Flashcards"):

        with st.spinner("Generating Flashcards..."):

            st.session_state.flashcards = generate_flashcards(pdf_text)
            st.session_state.current_card = 0
            st.session_state.show_answer = False

    if not st.session_state.flashcards:

        return

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