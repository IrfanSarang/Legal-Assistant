import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer


class Retriever:

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
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
    def retrieve(self, query: str, top_k: int = 2):

        if self.index is None or self.chunks is None:
            raise ValueError("Index not loaded. Call load() first.")

        # Embed query
        query_vector = self.model.encode([query])
        query_vector = np.array(query_vector).astype("float32")

        # 🔥 IMPORTANT: Normalize (since index uses cosine similarity)
        faiss.normalize_L2(query_vector)

        # Search
        distances, indices = self.index.search(query_vector, top_k)

        results = []

        for idx in indices[0]:
            if idx < len(self.chunks):
                results.append(self.chunks[idx])

        return results