from pypdf import PdfReader
import os
from app.contractRag.parser import IndianContractActParser
from app.contractRag.faiss_manager import ContractFAISSManager


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

PDF_PATH = os.path.join(
    BASE_DIR,
    "data",
    "contract",
    "indian_contract_act_1872.pdf"
)


def extract_pdf_text(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def main():

    print("📖 Extracting text from PDF...")

    if not os.path.exists(PDF_PATH):
        print("❌ File not found:", PDF_PATH)
        return

    text = extract_pdf_text(PDF_PATH)

    print("Text length:", len(text))

    # Parse
    parser = IndianContractActParser()
    sections = parser.parse(text)

    print("Total sections parsed:", len(sections))

    manager = ContractFAISSManager()
    manager.create_index(sections)

    print("✅ Ingestion complete.")


if __name__ == "__main__":
    main()