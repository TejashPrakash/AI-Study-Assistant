import hashlib


def get_pdf_hash(uploaded_file):
    """
    Returns a SHA256 hash of the uploaded PDF.
    """

    file_bytes = uploaded_file.getvalue()

    return hashlib.sha256(file_bytes).hexdigest()