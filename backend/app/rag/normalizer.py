import re
from typing import List, Dict, Any


class TextNormalizer:
    """
    Universal text normalizer.
    Can be extended for domain-specific cleaning.
    """

    def __init__(self, remove_patterns: List[str] = None):
        self.remove_patterns = remove_patterns or []

    def normalize_whitespace(self, text: str) -> str:
        # Normalize spaces but preserve paragraphs
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        return text.strip()

    def remove_custom_patterns(self, text: str) -> str:
        for pattern in self.remove_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        return text

    def clean_text(self, text: str) -> str:
        text = self.remove_custom_patterns(text)
        text = self.normalize_whitespace(text)
        return text

    def clean_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cleaned_docs = []

        for doc in documents:
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})

            cleaned_docs.append({
                "content": self.clean_text(content),
                "metadata": dict(metadata)
            })

        return cleaned_docs

class BNSNormalizer(TextNormalizer):
    """
    Legal Specific Cleaning layer.
    Extends universal normalizer
    """

    def remove_gazette_noise(self, text: str) -> str:
        patterns = [
            r'PUBLISHED BY AUTHORITY',
            r'REGISTERED NO\..*?\d{4}',
            r'EXTRAORDINARY',
            r'MINISTRY OF LAW AND JUSTICE.*?',
            r'No\.\s*\d+\]',
            r'NEW DELHI.*?\(SAKA\)',
            r'Separate paging is given.*?compilation\.',
            r'xxxGIDHxxx',
            r'xxxGIDExxx',
            r'vlk/kkj.k.*?',
            r'Hkkx.*?Section \d+',
            r'REGISTERED NO\..*?\d{4}',
        ]

        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

        return text

    def remove_hindi_garbage(self, text: str) -> str:
        words = text.split(" ")
        cleaned_words = []

        for word in words:
            if re.search(r'[a-z]{3,}[\/\'`]+[a-z]*', word):
                continue
            cleaned_words.append(word)

        return " ".join(cleaned_words)

    def fix_broken_uppercase_words(self, text: str) -> str:
        def fix_match(match):
            return match.group().replace(" ", "")

        pattern = r'(?:\b[A-Z]\s+){2,}[A-Z]\b'
        text = re.sub(pattern, fix_match, text)

        return text


    def clean_text(self, text: str) -> str:
        text = self.remove_gazette_noise(text)
        text = self.fix_broken_uppercase_words(text)
        text = self.remove_hindi_garbage(text)
        text = self.normalize_whitespace(text)
        return text
def remove_initial_gazette_pages(documents, skip_pages=1):
    return [
        doc for doc in documents
        if doc.get("metadata", {}).get("page", 0) > skip_pages
    ]


