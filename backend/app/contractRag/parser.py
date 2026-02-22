import re
from typing import List, Dict

class IndianContractActParser:
    # Pattern to match: "1. Title.—" or "19A. Title.—" or "Section 124. Title.—"
    SECTION_PATTERN = re.compile(
    r'^\s*(?:\d+\[)?(\d+[A-Z]?)\.?\s*[“"]?([A-Z][^.—\n]+)(?:[.—\-\s]|$)', 
    re.MULTILINE
    )

    def parse(self, text: str) -> List[Dict]:
        # 1. Skip the Index: Find where the actual law starts (usually Preamble or Section 1)
        start_marker = text.find("It is hereby enacted as follows")
        if start_marker != -1:
            text = text[start_marker:]
        
        matches = list(self.SECTION_PATTERN.finditer(text))
        sections = []
        
        for i, match in enumerate(matches):
            section_number = match.group(1).strip()
            title = match.group(2).strip()
            
            # 2. Extract Content: Everything between this match and the next match
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            content = text[start_pos:end_pos].strip()

            # 3. Filter Noise: Skip Repealed sections or empty titles
            if "[Repealed]" in title or "[Repealed]" in content:
                continue
            if not title or len(title) < 3:
                continue

            # 4. Contextual Metadata: Check for nearby Chapter or State info
            # We look back slightly from the match to see if a Chapter was just mentioned
            lookback = text[max(0, match.start()-100):match.start()]
            chapter_match = re.search(r'(CHAPTER\s+[IVXLC]+)', lookback)
            chapter = chapter_match.group(1) if chapter_match else "General"

            sections.append({
                "metadata": {
                    "document": "indian_contract_act_1872",
                    "section": section_number,
                    "chapter": chapter,
                    "is_amendment": "STATE AMENDMENT" in content
                },
                "title": title,
                "content": content,
                "chunk_text": f"Section {section_number}: {title}\n{content}"
            })

        print(f"✅ Extracted {len(sections)} valid legal sections.")
        return sections