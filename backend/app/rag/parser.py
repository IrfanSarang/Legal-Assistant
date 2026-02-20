import re
from typing import List, Dict, Any


class BNSSectionParser:
    """
    Robust section extractor for messy legal PDFs.
    """

    SECTION_PATTERN = re.compile(
        r'^\s*(\d{1,3}[A-Z]?)\.\s*(?:—|-)?\s*(.*)',
        re.MULTILINE
    )

    def split_into_sections(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        if not documents:
            return []

        full_text = "\n".join(doc.get("content", "") for doc in documents)

        matches = list(self.SECTION_PATTERN.finditer(full_text))

        structured_sections = []

        for i, match in enumerate(matches):
            section_number = match.group(1)
            section_title = match.group(2).strip()

            start = match.start()

            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(full_text)

            section_text = full_text[start:end].strip()

            structured_sections.append({
                "section_number": section_number,
                "section_title": section_title,
                "content": section_text,
                "metadata": {
                    "source": documents[0].get("metadata", {}).get("source"),
                    "type": "legal_section"
                }
            })

        return structured_sections
