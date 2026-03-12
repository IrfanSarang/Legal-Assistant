import re
from typing import List, Dict


# ---------------------------------------------------------------------------
# Private regex constants
# ---------------------------------------------------------------------------

_FOOTNOTE_ONLY_RE = re.compile(
    r'^\s*('
    r'See\s+s[s]?\.\s*\d'
    r'|Cf\.\s'
    r'|ibid\.'
    r'|As\s+to\s+'
    r'|For\s+(?:an\s+)?[Ee]xception'
    r')',
    re.IGNORECASE
)

_REPEALED_BOUNDARY_RE = re.compile(
    r'\[CHAPTER\s+[IVXLC]+[.\s][^\]]*\]\s*Rep\.'
    r'|CHAPTER\s+[IVXLC]+\.[—\s]\[?OF\s+PARTNERSHIP',
    re.IGNORECASE
)


# ---------------------------------------------------------------------------
# Parser class
# ---------------------------------------------------------------------------

class IndianContractActParser:
    """
    Parses the normalized full-text of the Indian Contract Act 1872 into
    a list of section dicts ready for chunking.

    Each section dict:
        metadata:
            document          : str   always "indian_contract_act_1872"
            section           : str   e.g. "10", "19A"
            chapter_id        : str   e.g. "CHAPTER II"
            chapter_title     : str   e.g. "OF CONTRACTS, VOIDABLE CONTRACTS..."
            has_illustrations : bool
            has_exceptions    : bool
            is_amendment      : bool
        title   : str   section heading
        content : str   full section body text
    """

    SECTION_PATTERN = re.compile(
        r'^\s*(\d+[A-Za-z]?)\.\s*(\u201c[^\n]{3,120}|[A-Z][^\n]{3,120})$',
        re.MULTILINE
    )
    CHAPTER_PATTERN = re.compile(
        r'CHAPTER\s{0,1}([IVXLC]+)\s*\n([^\n]+)',
        re.MULTILINE
    )
    REPEALED_RE = re.compile(r'\[Repealed\.?\]', re.IGNORECASE)

    # FIX-3: safer em-dash split — only split on .— or — with guard
    EMDASH_RE = re.compile(r'\s*\.?—\s*')

    # ------------------------------------------------------------------
    def _build_chapter_map(self, text: str) -> List[Dict]:
        chapters = []
        for m in self.CHAPTER_PATTERN.finditer(text):
            chapters.append({
                "pos":   m.start(),
                "id":    f"CHAPTER {m.group(1)}",
                "title": m.group(2).strip(),
            })
        return chapters

    def _get_chapter_for_pos(self, pos: int, chapter_map: List[Dict]) -> Dict:
        # FIX-4: always sort by position to handle any out-of-order captures
        current = {"id": "General", "title": "Preliminary"}
        for ch in sorted(chapter_map, key=lambda x: x["pos"]):
            if ch["pos"] <= pos:
                current = ch
            else:
                break
        return current

    def _split_title_content(self, title: str, content: str):
        """
        Split title at em-dash only if the overflow text is substantial
        body text (more than 15 chars). Prevents stripping valid title endings.
        """
        # FIX-3: guard against stripping valid title endings like "defined.—"
        emdash_match = self.EMDASH_RE.search(title)
        if emdash_match:
            overflow = title[emdash_match.end():].strip()
            title    = title[:emdash_match.start()].strip()
            if overflow and len(overflow) > 15:
                content = overflow + " " + content
        return title, content

    # ------------------------------------------------------------------
    def parse(self, text: str) -> List[Dict]:
        """
        Parse normalized full-document text into a list of section dicts.

        Args:
            text : normalized text from normalize_text()

        Returns:
            List of unique section dicts
        """
        # Skip table of contents — start from enactment clause
        start_marker = text.find("It is hereby enacted as follows")
        if start_marker != -1:
            text = text[start_marker:]
        else:
            print("[parser] Warning: enactment clause not found.")

        chapter_map = self._build_chapter_map(text)
        print(f"[parser] Found {len(chapter_map)} chapters.")
        for ch in chapter_map:
            print(f"         {ch['id']} — {ch['title']}")

        matches = list(self.SECTION_PATTERN.finditer(text))
        print(f"[parser] Found {len(matches)} raw section matches.")

        sections         = []
        skipped_repealed = 0
        skipped_footnote = 0

        for i, match in enumerate(matches):
            section_number = match.group(1).strip()
            title          = match.group(2).strip()

            start_pos = match.end()
            end_pos   = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            content   = text[start_pos:end_pos].strip()

            title, content = self._split_title_content(title, content)

            # Drop repealed sections
            if self.REPEALED_RE.search(title) or self.REPEALED_RE.search(content):
                skipped_repealed += 1
                continue

            if len(title) < 5:
                continue
            if len(content) < 10:
                continue

            # Drop pure footnote-reference content
            if _FOOTNOTE_ONLY_RE.match(content):
                skipped_footnote += 1
                continue

            # Truncate at repealed-chapter boundary
            bnd = _REPEALED_BOUNDARY_RE.search(content)
            if bnd:
                content = content[:bnd.start()].strip()
            if len(content) < 10:
                continue

            chapter = self._get_chapter_for_pos(match.start(), chapter_map)

            sections.append({
                "metadata": {
                    "document":          "indian_contract_act_1872",
                    "section":           section_number,
                    "chapter_id":        chapter["id"],
                    "chapter_title":     chapter["title"],
                    "has_illustrations": bool(re.search(r'\bIllustration[s]?\b', content, re.IGNORECASE)),
                    "has_exceptions":    bool(re.search(r'\bException\b',         content, re.IGNORECASE)),
                    "is_amendment":      bool(re.search(r'STATE AMENDMENT',       content, re.IGNORECASE)),
                },
                "title":   title,
                "content": content,
            })

        # FIX-5: deduplicate by section number — keeps first occurrence only
        seen    = set()
        deduped = []
        for sec in sections:
            sid = sec["metadata"]["section"]
            if sid not in seen:
                seen.add(sid)
                deduped.append(sec)
            else:
                print(f"[parser] ⚠️  Duplicate section {sid} dropped.")

        print(f"[parser] Skipped {skipped_repealed} repealed, {skipped_footnote} footnote-only.")
        print(f"[parser] ✅ Extracted {len(deduped)} unique sections.")
        return deduped