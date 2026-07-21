import streamlit as st

from src.services.notes_service import generate_notes
from src.services.export_service import generate_notes_pdf


def render_notes(uploaded_file, pdf_text):

    st.title("📝 Notes Generator")

    if not uploaded_file:

        st.warning("Please upload a PDF first.")

        return

    # Generate Notes
    if st.button("📝 Generate Notes"):

        with st.spinner("Generating Notes..."):

            st.session_state.notes = generate_notes(pdf_text)

    # Display Notes
    if st.session_state.notes:

        # Clean formatting issues
        notes = st.session_state.notes

        # Convert escaped newlines into actual new lines
        notes = notes.replace("\\n", "")

        # Remove escaped markdown characters
        notes = notes.replace("\\*", "*")

        # Ensure proper spacing between headings and content
        notes = notes.replace("## ", "## ")
        notes = notes.replace("### ", "### ")

        # Render properly formatted notes
        st.markdown(notes, unsafe_allow_html=True)

        st.divider()

        # Export as PDF
        pdf = generate_notes_pdf(notes)

        with open(pdf, "rb") as f:

            st.download_button(
                "📄 Download Notes as PDF",
                f,
                file_name="study_notes.pdf",
                mime="application/pdf",
                use_container_width=True
            )