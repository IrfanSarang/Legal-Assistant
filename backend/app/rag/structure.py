import re
from typing import List, Dict


# ------------------------------------------------------------
# Extract title and body
# ------------------------------------------------------------

def extract_title_and_body(section_number: str, content: str):
    # Remove section number
    content = re.sub(rf'^{section_number}\.\s*', '', content).strip()

    # Split first sentence
    sentences = re.split(r'\.\s+', content, maxsplit=1)

    if len(sentences) > 1:
        first_sentence = sentences[0].strip()

        # If first sentence is short enough → treat as title
        if len(first_sentence) < 120:
            title = first_sentence
            body = content[len(first_sentence):].strip()
            return title, body

    # Otherwise: no separate title
    return "", content



# ------------------------------------------------------------
# Extract illustrations
# ------------------------------------------------------------

def extract_illustrations(text: str):
    illustrations = []

    pattern = r'Illustrations?\.(.*?)(Explanation\.|Provided that|$)'
    match = re.search(pattern, text, re.DOTALL)

    if match:
        block = match.group(1)

        items = re.split(r'\(\d+\)', block)

        for item in items:
            clean = item.strip()
            if len(clean) > 20:
                illustrations.append(clean)

        text = text.replace(match.group(0), '')

    return text.strip(), illustrations


# ------------------------------------------------------------
# Extract explanations
# ------------------------------------------------------------

def extract_explanations(text: str):
    explanations = []

    pattern = r'Explanation\.?—?(.*?)(?=\n[A-Z]|\Z)'
    matches = re.findall(pattern, text, re.DOTALL)

    for match in matches:
        clean = match.strip()
        if len(clean) > 20:
            explanations.append(clean)

    text = re.sub(pattern, '', text, flags=re.DOTALL)

    return text.strip(), explanations


# ------------------------------------------------------------
# Extract provisos
# ------------------------------------------------------------

def extract_provisos(text: str):
    provisos = []

    matches = re.findall(r'Provided that(.*?)(?=\n[A-Z]|\Z)', text, re.DOTALL)

    for match in matches:
        clean = match.strip()
        if len(clean) > 20:
            provisos.append(clean)

    text = re.sub(r'Provided that.*?(?=\n[A-Z]|\Z)', '', text, flags=re.DOTALL)

    return text.strip(), provisos


# ------------------------------------------------------------
# Main Structuring Function
# ------------------------------------------------------------

def structure_sections(sections: List[Dict]) -> List[Dict]:
    structured = []

    for sec in sections:
        number = sec["section_number"]
        content = sec["content"]

        title, body = extract_title_and_body(number, content)
        body, illustrations = extract_illustrations(body)
        body, explanations = extract_explanations(body)
        body, provisos = extract_provisos(body)

        structured.append({
            "section_number": number,
            "title": title,
            "main_text": body,
            "illustrations": illustrations,
            "explanations": explanations,
            "provisos": provisos
        })

    return structured
