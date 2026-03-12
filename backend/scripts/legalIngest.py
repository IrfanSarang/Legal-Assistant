# scripts/ingest.py
# Run this ONCE from your project root:
# python -m scripts.legalIngest

import os
import sys

# Make sure app is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.loader import PDFLoader
from app.rag.normalizer import BNSNormalizer, remove_initial_gazette_pages
from app.rag.parser import BNSSectionParser
from app.rag.structure import structure_sections
from app.rag.chunker import chunk_structured_sections
from app.rag.faiss_manager import FAISSManager


def run_ingestion(
    pdf_path: str = "data/criminal/bns_2023/bns_2023.pdf",
    index_file: str = "data/faiss/faiss_index.bin",
    chunks_file: str = "data/faiss/chunks.pkl"
):
    print("=" * 50)
    print("BNS 2023 — RAG Ingestion Pipeline")
    print("=" * 50)

    # Step 1 — Load PDF
    print("\n[1/5] Loading PDF...")
    loader = PDFLoader(pdf_path)
    raw_docs = loader.load()
    print(f"      Pages loaded: {len(raw_docs)}")

    # Step 2 — Normalize
    print("\n[2/5] Normalizing text...")
    normalizer = BNSNormalizer()
    filtered = remove_initial_gazette_pages(raw_docs, skip_pages=1)
    cleaned = normalizer.clean_documents(filtered)
    print(f"      Pages after cleaning: {len(cleaned)}")

    # Step 3 — Parse sections
    print("\n[3/5] Parsing sections...")
    parser = BNSSectionParser()
    sections = parser.split_into_sections(cleaned)
    print(f"      Sections found: {len(sections)}")

    # Step 4 — Structure + Chunk
    print("\n[4/5] Structuring and chunking...")
    structured = structure_sections(sections)
    chunks = chunk_structured_sections(structured)
    print(f"      Total chunks: {len(chunks)}")

    # Step 5 — Build FAISS index
    print("\n[5/5] Building FAISS index...")
    manager = FAISSManager(
        index_file=index_file,
        chunks_file=chunks_file
    )
    manager.create_index(chunks)

    print("\n" + "=" * 50)
    print("✅ Ingestion complete!")
    print(f"   Index : {index_file}")
    print(f"   Chunks: {chunks_file}")
    print("=" * 50)
    print("\nYou can now start your FastAPI server.")
    print("The server will load the index automatically on startup.")


if __name__ == "__main__":
    run_ingestion()