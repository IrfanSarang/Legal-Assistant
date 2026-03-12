import os
from typing import List, Dict
from pypdf import PdfReader


def load_pdf_with_metadata(file_path: str, skip_pages: int = 0) -> List[Dict]:
    """
    Load a PDF and return a list of page dicts.

    Each dict has:
        page   : int   — 1-based page number
        text   : str   — extracted text
        source : str   — filename

    Args:
        file_path   : absolute or relative path to the PDF file
        skip_pages  : number of pages to skip from the start (default 0)

    Returns:
        List of page dicts (only pages with non-empty text are included)

    Raises:
        ValueError        if file is not a PDF
        FileNotFoundError if file does not exist
    """
    if not file_path.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported.")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    reader   = PdfReader(file_path)
    pages    = []
    filename = os.path.basename(file_path)

    for page_number, page in enumerate(reader.pages):
        if page_number < skip_pages:
            continue
        text = page.extract_text()
        if text and text.strip():
            pages.append({
                "page":   page_number + 1,
                "text":   text.strip(),
                "source": filename,
            })

    print(f"[loader] ✅ Loaded {len(pages)} pages from '{filename}'")
    return pages