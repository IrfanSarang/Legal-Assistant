import re
from typing import List, Dict

# Better legal sentence splitter
LEGAL_SENTENCE_SPLIT = re.compile(
    r'(?<=[.!?])\s+'
)

def structure_sections_for_rag(
    sections: List[Dict],
    max_chunk_chars: int = 1500,
    overlap_chars: int = 300
) -> List[Dict]:

    structured_chunks = []

    for sec in sections:
        section_prefix = (
            f"Indian Contract Act 1872 | "
            f"Section {sec.get('section')} | "
            f"{sec.get('title', '').strip()}.\n"
        )

        # Normalize whitespace
        content = re.sub(r'\s+', ' ', sec.get("content", "")).strip()

        if not content:
            continue

        sentences = LEGAL_SENTENCE_SPLIT.split(content)

        current_chunk = ""
        chunk_index = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # If adding sentence exceeds limit → finalize chunk
            if len(current_chunk) + len(sentence) > max_chunk_chars:

                if current_chunk.strip():

                    structured_chunks.append({
                        "metadata": {
                            **sec,
                            "chunk_index": chunk_index
                        },
                        "embedding_text": section_prefix + current_chunk.strip(),
                        "content": current_chunk.strip()
                    })

                    chunk_index += 1

                # Create overlap safely
                if overlap_chars > 0 and len(current_chunk) > overlap_chars:
                    current_chunk = current_chunk[-overlap_chars:] + " " + sentence
                else:
                    current_chunk = sentence
            else:
                current_chunk += " " + sentence

        # Add last chunk
        if current_chunk.strip():
            structured_chunks.append({
                "metadata": {
                    **sec,
                    "chunk_index": chunk_index
                },
                "embedding_text": section_prefix + current_chunk.strip(),
                "content": current_chunk.strip()
            })

    return structured_chunks