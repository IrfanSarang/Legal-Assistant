import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer


class Retriever:

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-mpnet-base-v2",
        vector_store_path: str = "./data/vector_store"
    ):
        self.model = SentenceTransformer(model_name)
        self.vector_store_path = vector_store_path

        self.index_path = os.path.join(
            self.vector_store_path,
            "faiss_index.bin"
        )

        self.chunks_path = os.path.join(
            self.vector_store_path,
            "chunks.pkl"
        )

        self.index = None
        self.chunks = None

    # -----------------------------
    # LOAD INDEX + METADATA
    # -----------------------------
    def load(self):

        if not os.path.exists(self.index_path):
            raise FileNotFoundError("FAISS index not found.")

        if not os.path.exists(self.chunks_path):
            raise FileNotFoundError("Chunks metadata not found.")

        # Load FAISS index
        self.index = faiss.read_index(self.index_path)

        # Load chunk metadata (pickle!)
        with open(self.chunks_path, "rb") as f:
            self.chunks = pickle.load(f)

        print(f"✅ Retriever loaded ({self.index.ntotal} vectors).")

    # -----------------------------
    # SEARCH FUNCTION
    # -----------------------------
    def retrieve(self, query: str, top_k: int = 5):
        if self.index is None or self.chunks is None:
            raise ValueError("Index not loaded. Call load() first.")

        # Fetch more candidates then deduplicate
        fetch_k = top_k * 4
        query_vector = self.model.encode([query])
        query_vector = np.array(query_vector).astype("float32")
        faiss.normalize_L2(query_vector)

        distances, indices = self.index.search(query_vector, fetch_k)

        results = []
        seen_sections = set()

        for idx in indices[0]:
            if idx < len(self.chunks):
                chunk = self.chunks[idx]
                section_id = chunk.get("metadata", {}).get("section", idx)
                if section_id not in seen_sections:
                    seen_sections.add(section_id)
                    results.append(chunk)
                if len(results) >= top_k:
                    break

        return results