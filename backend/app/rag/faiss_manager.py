# app/rag/faiss_manager.py
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class FAISSManager:
    def __init__(self, embedding_model_name="all-MiniLM-L6-v2",
                 index_file="data/faiss/faiss_index.bin",
                 chunks_file="data/faiss/chunks.pkl"):
        self.model = SentenceTransformer(embedding_model_name)
        self.index_file = index_file
        self.chunks_file = chunks_file
        self.index = None
        self.chunked_sections = []

    # -----------------------------
    # One-time ingestion: create index
    # -----------------------------
    def create_index(self, chunked_sections: List[Dict]):
        print("Generating embeddings for chunks...")
        texts = [c["chunk_text"] for c in chunked_sections]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        # Save to disk
        faiss.write_index(index, self.index_file)
        with open(self.chunks_file, "wb") as f:
            pickle.dump(chunked_sections, f)

        print(f"FAISS index saved with {index.ntotal} vectors.")
        self.index = index
        self.chunked_sections = chunked_sections

    # -----------------------------
    # Load index from disk
    # -----------------------------
    def load_index(self):
        self.index = faiss.read_index(self.index_file)
        with open(self.chunks_file, "rb") as f:
            self.chunked_sections = pickle.load(f)
        print(f"FAISS index loaded with {self.index.ntotal} vectors.")

    # -----------------------------
    # Query function
    # -----------------------------
    def query(self, query_text: str, top_k: int = 3) -> List[Dict]:
        if self.index is None:
            raise ValueError("Index not loaded. Run load_index() first.")

        query_vec = self.model.encode([query_text]).astype("float32")
        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for idx in indices[0]:
            results.append(self.chunked_sections[idx])

        return results
