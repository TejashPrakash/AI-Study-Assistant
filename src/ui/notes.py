import streamlit as st

from src.services.notes_service import generate_notes


def render_notes(uploaded_file, pdf_text):

    st.title("📝 Notes Generator")

    if not uploaded_file:

        st.warning("Please upload a PDF first.")

        return

    if st.button("📝 Generate Notes"):

        with st.spinner("Generating Notes..."):

            st.session_state.notes = generate_notes(pdf_text)

    if st.session_state.notes:

        st.markdown(st.session_state.notes)

        st.download_button(
            "⬇ Download Notes",
            st.session_state.notes,
            file_name="study_notes.md",
            mime="text/markdown"
        )