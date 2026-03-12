import re

def normalize_text(text: str) -> str:
    """
    Clean raw PDF text for downstream parsing and chunking.

    Steps:
        1. Standardize line endings
        2. Remove footnote number markers e.g. 1[ 2[
        3. Remove orphaned closing brackets
        4. Remove legislative noise lines   (Subs., Rep., Ins., See s., ibid., ...)
        5. Remove standalone page numbers
        6. Fix hyphen line-breaks           e.g. "pro-\nmise" → "promise"
        7. Remove PDF footnote artefacts    e.g. 3***, 4***
        8. Normalize whitespace

    Args:
        text : raw text string (typically the full document or a page)

    Returns:
        Cleaned text string
    """
    # 1. Standardize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # 2. Remove footnote number markers e.g. 1[ 2[
    text = re.sub(r'\d+$', '', text)

    # 3. Remove orphaned closing brackets
    text = re.sub(r'\s+$\s*', ' ', text)

    # 4. Remove legislative noise lines
    noise_pattern = re.compile(
        r'^\s*\d*\.?\s*(Subs\.|Rep\.|Ins\.|See s\.|ibid\.)',
        re.IGNORECASE | re.MULTILINE
    )
    cleaned_lines = [
        line for line in text.split('\n')
        if not noise_pattern.match(line)
    ]
    text = '\n'.join(cleaned_lines)

    # 5. Remove standalone page numbers
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

    # 6. Fix hyphen line-breaks
    text = re.sub(r'-\n(\w)', r'\1', text)

    # 7. Remove PDF footnote artefacts like 3***, 4***
    text = re.sub(r'\d+\*+', '', text)
    text = re.sub(
        r'\b(rep\.|subs\.|ins\.).*?(?:\.\s|\n)',
        ' ',
        text,
        flags=re.IGNORECASE | re.MULTILINE
    )

    # 8. Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()
