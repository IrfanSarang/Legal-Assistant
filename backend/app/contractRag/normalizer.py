import re

def normalize_text(text: str) -> str:
    # 1. Standardize line endings
    text = text.replace('\r', '')

    # 2. Fix PDF "Word Fragmentation" 
    # Fixes: "ex istence" -> "existence", "t ransaction" -> "transaction"
    text = re.sub(r'(\w)\s+(\w{1,3})\s+(\w)', r'\1\2\3', text)

    # 3. Strip Footnote Brackets (e.g., "1[15." -> "15.")
    text = re.sub(r'\d+\[', '', text)

    # 4. Remove standalone Page Numbers
    # Only if the number is on its own line and NOT followed by a dot (section marker)
    text = re.sub(r'^\s*\d+\s*$(?!\.)', '', text, flags=re.MULTILINE)

    # 5. Remove "Subs. by" legislative noise (historical footnotes)
    text = re.sub(r'Subs\. by .*?ibid\.', '', text, flags=re.IGNORECASE | re.DOTALL)

    # 6. Standardize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()