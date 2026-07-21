import base64
import streamlit as st


def render_pdf_viewer(uploaded_file):

    if not uploaded_file:
        return

    uploaded_file.seek(0)

    pdf_bytes = uploaded_file.read()

    uploaded_file.seek(0)

    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

    pdf_display = f"""
    <iframe
        src="data:application/pdf;base64,{pdf_base64}"
        width="100%"
        height="850"
        type="application/pdf">
    </iframe>
    """

    st.markdown(pdf_display, unsafe_allow_html=True)