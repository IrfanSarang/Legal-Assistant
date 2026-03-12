import re
from typing import List, Dict


def extract_title_and_body(section_number: str, content: str):
    content = re.sub(rf'^{section_number}\.\s*', '', content).strip()
    sentences = re.split(r'\.\s+', content, maxsplit=1)
    if len(sentences) > 1 and len(sentences[0].strip()) < 120:
        title = sentences[0].strip()
        body = content[len(title):].strip()
        return title, body
    return "", content


def extract_illustrations(text: str):
    illustrations = []
    pattern = r'Illustrations?\.(.*?)(Explanation\.|Provided that|$)'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        block = match.group(1)
        items = re.split(r'\(\d+\)', block)
        illustrations = [i.strip() for i in items if len(i.strip()) > 20]
        text = text.replace(match.group(0), '')
    return text.strip(), illustrations


def extract_explanations(text: str):
    explanations = []
    pattern = r'Explanation\.?—?(.*?)(?=\n[A-Z]|\Z)'
    matches = re.findall(pattern, text, re.DOTALL)
    explanations = [m.strip() for m in matches if len(m.strip()) > 20]
    text = re.sub(pattern, '', text, flags=re.DOTALL)
    return text.strip(), explanations


def extract_provisos(text: str):
    provisos = []
    matches = re.findall(r'Provided that(.*?)(?=\n[A-Z]|\Z)', text, re.DOTALL)
    provisos = [m.strip() for m in matches if len(m.strip()) > 20]
    text = re.sub(r'Provided that.*?(?=\n[A-Z]|\Z)', '', text, flags=re.DOTALL)
    return text.strip(), provisos


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