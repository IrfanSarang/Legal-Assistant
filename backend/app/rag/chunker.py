from typing import List, Dict


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """
    Split text into overlapping word chunks.
    """
    words = text.split()
    chunks = []
    start = 0
    total_words = len(words)

    while start < total_words:
        end = min(start + chunk_size, total_words)
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - chunk_overlap

    return chunks


def chunk_structured_sections(
    structured_sections: List[Dict],
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> List[Dict]:
    """
    Take structured sections and split main_text into chunks.
    """
    chunked_sections = []

    for sec in structured_sections:
        main_text_chunks = chunk_text(
            sec["main_text"],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        for i, chunk in enumerate(main_text_chunks):
            chunked_sections.append({
                "section_number": sec["section_number"],
                "title": sec["title"],
                "chunk_index": i,
                "chunk_text": chunk,
                "illustrations": sec["illustrations"],
                "explanations": sec["explanations"],
                "provisos": sec["provisos"],
            })

    return chunked_sections
