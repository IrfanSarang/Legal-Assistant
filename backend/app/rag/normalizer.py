import re
from typing import List, Dict, Any


class BNSNormalizer:

    def normalize_whitespace(self, text: str) -> str:
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        return text.strip()

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
        ]
        for p in patterns:
            text = re.sub(p, '', text, flags=re.IGNORECASE)
        return text

    def remove_hindi_garbage(self, text: str) -> str:
        words = text.split(" ")
        return " ".join(
            w for w in words
            if not re.search(r'[a-z]{3,}[\/\'`]+[a-z]*', w)
        )

    def fix_broken_uppercase_words(self, text: str) -> str:
        def fix_match(m):
            return m.group().replace(" ", "")
        return re.sub(r'(?:\b[A-Z]\s+){2,}[A-Z]\b', fix_match, text)

    def clean_text(self, text: str) -> str:
        text = self.remove_gazette_noise(text)
        text = self.fix_broken_uppercase_words(text)
        text = self.remove_hindi_garbage(text)
        text = self.normalize_whitespace(text)
        return text

    def clean_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [{
            "content": self.clean_text(doc.get("content", "")),
            "metadata": dict(doc.get("metadata", {}))
        } for doc in documents]


def remove_initial_gazette_pages(documents: List[Dict[str, Any]], skip_pages: int = 1):
    return [
        doc for doc in documents
        if doc.get("metadata", {}).get("page", 0) > skip_pages
    ]