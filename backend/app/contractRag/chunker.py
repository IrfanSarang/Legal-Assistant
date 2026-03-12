import re
from typing import List, Dict


# Sentence boundary splitter — splits on . ! ? followed by whitespace
LEGAL_SENTENCE_SPLIT = re.compile(r'(?<=[.!?])\s+')


def structure_sections_for_rag(
    sections:        List[Dict],
    max_chunk_chars: int = 1500,
    overlap_chars:   int = 300,
) -> List[Dict]:
    """
    Split parsed sections into overlapping chunks for RAG embedding.

    Each output chunk dict:
        metadata:
            (all fields from section metadata, plus)
            chunk_index : int   0-based index within the section
            title       : str   section title
        embedding_text : str   text sent to the embedding model
                               (prefix + content)
        content        : str   raw section text for this chunk

    Args:
        sections        : list of section dicts from IndianContractActParser
        max_chunk_chars : maximum characters per chunk body (default 1500)
        overlap_chars   : characters of overlap between consecutive chunks
                          within the same section (default 300)

    Returns:
        List of chunk dicts
    """
    structured_chunks = []

    for sec in sections:
        metadata = sec["metadata"]
        title    = sec.get("title", "").strip()
        content  = sec.get("content", "").strip()

        if not content:
            continue

        # FIX-4: include chapter context in embedding prefix.
        #        Preliminary/General sections (before Chapter I) use a label.
        ch_label = (
            f"{metadata['chapter_id']} — {metadata['chapter_title']}"
            if metadata["chapter_id"] != "General"
            else "Preliminary Provisions"
        )
        section_prefix = (
            f"Indian Contract Act 1872 | "
            f"{ch_label} | "
            f"Section {metadata['section']} | "
            f"{title}.\n"
        )

        # Collapse internal whitespace before splitting into sentences
        content   = re.sub(r'\s+', ' ', content)
        sentences = LEGAL_SENTENCE_SPLIT.split(content)

        current_chunk = ""
        chunk_index   = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if len(current_chunk) + len(sentence) > max_chunk_chars:
                if current_chunk.strip():
                    structured_chunks.append({
                        "metadata": {
                            **metadata,
                            "chunk_index": chunk_index,
                            "title":       title,
                        },
                        "embedding_text": section_prefix + current_chunk.strip(),
                        "content":        current_chunk.strip(),
                    })
                    chunk_index += 1

                # Carry overlap from end of previous chunk
                if overlap_chars > 0 and len(current_chunk) > overlap_chars:
                    current_chunk = current_chunk[-overlap_chars:] + " " + sentence
                else:
                    current_chunk = sentence
            else:
                current_chunk += " " + sentence

        # Flush the last chunk
        if current_chunk.strip():
            structured_chunks.append({
                "metadata": {
                    **metadata,
                    "chunk_index": chunk_index,
                    "title":       title,
                },
                "embedding_text": section_prefix + current_chunk.strip(),
                "content":        current_chunk.strip(),
            })

    print(f"[chunker] ✅ Produced {len(structured_chunks)} chunks.")
    return structured_chunks