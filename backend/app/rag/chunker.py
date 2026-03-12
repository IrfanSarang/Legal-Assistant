import re
from typing import List, Dict


def chunk_text(text: str, chunk_size: int = 200, chunk_overlap: int = 40) -> List[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - chunk_overlap
    return chunks


def clean_gazette_noise_from_text(text: str) -> str:
    patterns = [
        r'Sec\.\s*1\]\s*THE GAZETTE OF INDIA.*?_{10,}',
        r'THE GAZETTE OF INDIA.*?\n',
        r'Abetment of a\nthing\.\nAbettor\.',
        r'Punishment\nfor belonging\nto gang.*?\n',
        r'Dishonest\nmisappropriation\nofproperty\.',
    ]
    for p in patterns:
        text = re.sub(p, '', text, flags=re.IGNORECASE | re.DOTALL)
    return text.strip()


def split_by_subitems(text: str) -> List[str]:
    items = re.split(r'\n?\([a-z]\)\s*', text)
    return [item.strip() for item in items if len(item.strip().split()) > 10]


def force_chunk_by_words(text: str, prefix: str, chunk_size: int = 150) -> List[str]:
    chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=20)
    return [prefix + c for c in chunks if len(c.split()) > 15]


def chunk_structured_sections(
    structured_sections: List[Dict],
    chunk_size: int = 200,
    chunk_overlap: int = 40
) -> List[Dict]:

    chunked_sections = []

    for sec in structured_sections:
        sec_num = sec["section_number"]
        title = sec["title"]
        prefix = f"Section {sec_num}: {title}. " if title else f"Section {sec_num}. "

        # --- Main text chunks ---
        for i, chunk in enumerate(chunk_text(sec["main_text"], chunk_size, chunk_overlap)):
            if len(chunk.split()) < 20:
                continue
            chunked_sections.append({
                "section_number": sec_num,
                "title": title,
                "chunk_index": f"{i}",
                "chunk_type": "main_text",
                "chunk_text": prefix + chunk,
            })

        # --- Illustration chunks ---
        for j, illus in enumerate(sec["illustrations"]):
            if len(illus.split()) < 10:
                continue
            illus = clean_gazette_noise_from_text(illus)
            if len(illus.split()) > 150:
                sub_items = split_by_subitems(illus)
                if sub_items:
                    for k, sub in enumerate(sub_items):
                        if len(sub.split()) > 200:
                            for m, fc in enumerate(force_chunk_by_words(sub, prefix + "Illustration: ")):
                                chunked_sections.append({
                                    "section_number": sec_num,
                                    "title": title,
                                    "chunk_index": f"{j}-{k}-{m}",
                                    "chunk_type": "illustration",
                                    "chunk_text": fc,
                                })
                        elif len(sub.split()) >= 10:
                            chunked_sections.append({
                                "section_number": sec_num,
                                "title": title,
                                "chunk_index": f"{j}-{k}",
                                "chunk_type": "illustration",
                                "chunk_text": prefix + "Illustration: " + sub,
                            })
                else:
                    for k, fc in enumerate(force_chunk_by_words(illus, prefix + "Illustration: ")):
                        chunked_sections.append({
                            "section_number": sec_num,
                            "title": title,
                            "chunk_index": f"{j}-{k}",
                            "chunk_type": "illustration",
                            "chunk_text": fc,
                        })
            else:
                chunked_sections.append({
                    "section_number": sec_num,
                    "title": title,
                    "chunk_index": f"{j}",
                    "chunk_type": "illustration",
                    "chunk_text": prefix + "Illustration: " + illus,
                })

        # --- Explanation chunks ---
        for k, expl in enumerate(sec["explanations"]):
            if len(expl.split()) < 10:
                continue
            expl = clean_gazette_noise_from_text(expl)
            if len(expl.split()) > 150:
                sub_items = split_by_subitems(expl)
                if sub_items:
                    for m, sub in enumerate(sub_items):
                        if len(sub.split()) > 200:
                            for n, fc in enumerate(force_chunk_by_words(sub, prefix + "Explanation: ")):
                                chunked_sections.append({
                                    "section_number": sec_num,
                                    "title": title,
                                    "chunk_index": f"{k}-{m}-{n}",
                                    "chunk_type": "explanation",
                                    "chunk_text": fc,
                                })
                        elif len(sub.split()) >= 10:
                            chunked_sections.append({
                                "section_number": sec_num,
                                "title": title,
                                "chunk_index": f"{k}-{m}",
                                "chunk_type": "explanation",
                                "chunk_text": prefix + "Explanation: " + sub,
                            })
                else:
                    for m, fc in enumerate(force_chunk_by_words(expl, prefix + "Explanation: ")):
                        chunked_sections.append({
                            "section_number": sec_num,
                            "title": title,
                            "chunk_index": f"{k}-{m}",
                            "chunk_type": "explanation",
                            "chunk_text": fc,
                        })
            else:
                chunked_sections.append({
                    "section_number": sec_num,
                    "title": title,
                    "chunk_index": f"{k}",
                    "chunk_type": "explanation",
                    "chunk_text": prefix + "Explanation: " + expl,
                })

    return chunked_sections