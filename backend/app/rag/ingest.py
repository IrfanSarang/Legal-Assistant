from dotenv import load_dotenv
from collections import defaultdict
from app.rag.extractor import load_all
from app.rag.splitter import splitter
from app.rag.embedder import create_vector

load_dotenv()

if __name__ == "__main__":
    print("\n============================")
    print("Ingestion Process started....")

    print("Loading documents and producing chunks...")
    docs = load_all("data")
    chunks = splitter(docs)

    # Group chunks by category to create namespaces
    grouped_chunks = defaultdict(list)
    for chunk in chunks:
        # Assumes extractor.py set 'category' in metadata
        category = chunk.metadata.get("category", "default")
        grouped_chunks[category].append(chunk)

    print("============================")
    print("Generating Embeddings per Namespace...")
    
    for category, cat_chunks in grouped_chunks.items():
        print(f"Uploading to namespace: {category}...")
        create_vector(cat_chunks, namespace=category)

    print("============================")
    print("Successfully Completed Ingestion Process!!")