# app/services/loader.py

import os
from pypdf import PdfReader


def load_pdf(file_path: str, skip_pages: int = 0) -> str:
    """
    Loads only PDF files and returns extracted text.
    skip_pages applies to PDFs.
    """

    if not file_path.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported.")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    reader = PdfReader(file_path)
    full_text = []

    for page_number, page in enumerate(reader.pages):
        if page_number < skip_pages:
            continue

        text = page.extract_text()

        if text:
            full_text.append(text)

    return "\n".join(full_text)