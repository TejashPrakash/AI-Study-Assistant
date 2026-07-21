import streamlit as st

from src.services.notes_service import generate_notes
from src.services.export_service import generate_notes_pdf


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

        pdf = generate_notes_pdf(
            st.session_state.notes
        )

        with open(pdf, "rb") as f:

            st.download_button(
                "📄 Download Notes as PDF",
                f,
                file_name="study_notes.pdf",
                mime="application/pdf",
                use_container_width=True
            )