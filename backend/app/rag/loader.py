from pathlib import Path
from typing import List, Dict, Any
from pypdf import PdfReader


class PDFLoader:
    """
    Universal PDF Loader.
    Extracts page-wise raw text with metadata.
    No domain-specific cleaning here.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    def load(self) -> List[Dict[str, Any]]:
        reader = PdfReader(str(self.file_path))
        documents = []

        total_pages = len(reader.pages)

        for page_number, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text()
            except Exception:
                continue

            if not text:
                continue

            text = text.strip()

            documents.append({
                "content": text,
                "metadata": {
                    "source": self.file_path.name,
                    "doc_id": self.file_path.stem,
                    "page": page_number,
                    "total_pages": total_pages
                }
            })

        return documents
