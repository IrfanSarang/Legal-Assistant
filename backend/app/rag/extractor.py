import os
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, Docx2txtLoader

SUPPORTED_EXTENSIONS = [".pdf", ".txt", ".docx"]

def load_file(path):
    ext = os.path.splitext(path)[-1].lower()

    if ext == ".pdf":
        return PyMuPDFLoader(path, mode="single").load()
    elif ext == ".txt":
        return TextLoader(path, encoding="utf-8").load()
    elif ext == ".docx":
        return Docx2txtLoader(path).load()
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def load_all(root_folder = "data"):
    all_docs = []

    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            ext = os.path.splitext(filename)[-1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                filepath = os.path.join(dirpath, filename)
                print(f"Loading: {filepath}")
                try: 
                    docs = load_file(filepath)

                    category = os.path.basename(dirpath)
                    for doc in docs:
                        doc.metadata["category"] = category
                        doc.metadata["filename"] = filename
                        doc.metadata["source"] = filepath
                    
                    all_docs.extend(docs)
                except Exception as e:
                    print(f"Skipped {filepath} — {e}")

    print(f"\nTotal documents loaded: {len(all_docs)}")
    return all_docs

