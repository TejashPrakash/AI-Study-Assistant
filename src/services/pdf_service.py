import streamlit as st

from src.utils.pdf_loader import extract_text_from_pdf
from src.utils.pdf_utils import get_pdf_hash
from src.utils.cache_manager import pdf_exists, add_pdf
from src.utils.text_splitter import split_text
from src.embeddings import create_embeddings
from src.vector_store import store_chunks
from src.config import TOP_K


def process_pdf(uploaded_file):

    if not uploaded_file:
        return None

    pdf_hash = get_pdf_hash(uploaded_file)

    pdf_text = extract_text_from_pdf(uploaded_file)

    chunks = []

    if not pdf_exists(pdf_hash):

        with st.spinner("📄 Processing PDF..."):

            chunks = split_text(pdf_text)

            embeddings = create_embeddings(chunks)

            store_chunks(chunks, embeddings)

            add_pdf(pdf_hash)

        st.sidebar.success("✅ PDF Indexed Successfully")

    else:

        st.sidebar.success("⚡ PDF Already Indexed")

        chunks = split_text(pdf_text)

    st.sidebar.markdown("---")
    st.sidebar.metric("Chunks", len(chunks))
    st.sidebar.metric("Top K", TOP_K)

    return pdf_text