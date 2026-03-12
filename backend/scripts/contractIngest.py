# scripts/ingest.py
# Run this ONCE from your project root:
#   python -m scripts.contractIngest

import os
import sys
import time

# Make sure app is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.contractRag.loader        import load_pdf_with_metadata
from app.contractRag.normalizer    import normalize_text
from app.contractRag.parser        import IndianContractActParser
from app.contractRag.enricher      import enrich_sections
from app.contractRag.chunker       import structure_sections_for_rag
from app.contractRag.faiss_manager import ContractFAISSManager

from sentence_transformers import SentenceTransformer


def run_ingestion(
    pdf_path:    str = "data/contract/indian_contract_act_1872.pdf",
    index_file:  str = "data/vector_store/faiss_index.bin",
    chunks_file: str = "data/vector_store/chunks.pkl",
    model_name:  str = "sentence-transformers/all-mpnet-base-v2",
    model_cache: str = "data/model_cache",
    chunk_size:  int = 1500,
    overlap:     int = 300,
):
    t_start = time.time()

    print("=" * 50)
    print("Indian Contract Act 1872 — RAG Ingestion Pipeline")
    print("=" * 50)

    # ── Step 1: Load PDF ─────────────────────────────────────────────────────
    print("\n[1/5] Loading PDF...")
    pages = load_pdf_with_metadata(pdf_path)
    print(f"      Pages loaded : {len(pages)}")
    print(f"      Source file  : {os.path.basename(pdf_path)}")

    # ── Step 2: Normalize text ────────────────────────────────────────────────
    print("\n[2/5] Normalizing text...")
    raw_text   = "\n".join(p["text"] for p in pages)
    clean_text = normalize_text(raw_text)
    removed    = len(raw_text) - len(clean_text)
    print(f"      Raw chars    : {len(raw_text):,}")
    print(f"      Clean chars  : {len(clean_text):,}")
    print(f"      Removed      : {removed:,} chars")

    # ── Step 3: Parse sections ────────────────────────────────────────────────
    print("\n[3/5] Parsing sections...")
    parser   = IndianContractActParser()
    sections = parser.parse(clean_text)
    print(f"      Sections found: {len(sections)}")

    # ── Step 3.5: Enrich sections with legal keywords ─────────────────────────
    print("\n[3.5/5] Enriching sections with legal concept keywords...")
    sections = enrich_sections(sections)

    # ── Step 4: Chunk ─────────────────────────────────────────────────────────
    print("\n[4/5] Chunking sections...")
    chunks = structure_sections_for_rag(
        sections,
        max_chunk_chars = chunk_size,
        overlap_chars   = overlap,
    )
    lengths = [len(c["content"]) for c in chunks]
    print(f"      Total chunks : {len(chunks)}")
    print(f"      Min length   : {min(lengths)} chars")
    print(f"      Avg length   : {int(sum(lengths)/len(lengths))} chars")
    print(f"      Max length   : {max(lengths)} chars")

    # ── Step 5: Build FAISS index ─────────────────────────────────────────────
    print("\n[5/5] Building FAISS index...")

    # Load model from local cache if available, else download once
    local_model_path = os.path.join(model_cache, model_name)
    if os.path.isdir(local_model_path):
        print(f"      Loading model from cache: {local_model_path}")
        model = SentenceTransformer(local_model_path)
    else:
        print(f"      Downloading model '{model_name}' (one-time)...")
        os.makedirs(model_cache, exist_ok=True)
        model = SentenceTransformer(model_name)
        model.save(local_model_path)
        print(f"      Model cached at: {local_model_path}")

    # Create output directory if needed
    os.makedirs(os.path.dirname(index_file),  exist_ok=True)
    os.makedirs(os.path.dirname(chunks_file), exist_ok=True)

    manager = ContractFAISSManager(
        model             = model,
        vector_store_path = os.path.dirname(index_file),
    )
    manager.create_index(chunks)

    elapsed = time.time() - t_start

    print("\n" + "=" * 50)
    print("✅ Ingestion complete!")
    print(f"   Sections : {len(sections)}")
    print(f"   Chunks   : {len(chunks)}")
    print(f"   Vectors  : {manager.index.ntotal}")
    print(f"   Index    : {index_file}")
    print(f"   Chunks   : {chunks_file}")
    print(f"   Time     : {elapsed:.1f}s")
    print("=" * 50)
    print("\nYou can now start your FastAPI server.")
    print("The server will load the index automatically on startup.")


if __name__ == "__main__":
    run_ingestion()