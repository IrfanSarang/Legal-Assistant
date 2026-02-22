import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from typing import List, Dict


class ContractFAISSManager:

    def __init__(
        self,
        embedding_model_name: str = "all-MiniLM-L6-v2",
    ):
        self.base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        self.vector_dir = os.path.join(
            self.base_dir, "data", "vector_store"
        )

        self.index_file = os.path.join(
            self.vector_dir, "faiss_index.bin"
        )

        self.chunks_file = os.path.join(
            self.vector_dir, "chunks.pkl"
        )

        self.model = SentenceTransformer(embedding_model_name)

        self.index = None
        self.chunked_sections = []

    # -----------------------------
    # One-time ingestion
    # -----------------------------
    def create_index(self, chunked_sections: List[Dict]):

        os.makedirs(self.vector_dir, exist_ok=True)

        print("Generating embeddings...")

        # 🔥 Match first manager
        texts = [c["chunk_text"] for c in chunked_sections]

        embeddings = self.model.encode(texts, show_progress_bar=True)
        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]

        # 🔥 Use L2 distance (like first version)
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        faiss.write_index(index, self.index_file)

        with open(self.chunks_file, "wb") as f:
            pickle.dump(chunked_sections, f)

        print(f"FAISS index saved with {index.ntotal} vectors.")

        self.index = index
        self.chunked_sections = chunked_sections

    # -----------------------------
    # Load index
    # -----------------------------
    def load_index(self):

        if not os.path.exists(self.index_file):
            raise FileNotFoundError(
                "FAISS index not found. Run create_index() first."
            )

        self.index = faiss.read_index(self.index_file)

        with open(self.chunks_file, "rb") as f:
            self.chunked_sections = pickle.load(f)

        print(f"FAISS index loaded with {self.index.ntotal} vectors.")

    # -----------------------------
    # Query
    # -----------------------------
    def query(self, query_text: str, top_k: int = 2) -> List[Dict]:

        if self.index is None:
            self.load_index()

        query_vec = self.model.encode([query_text]).astype("float32")

        # ❌ No normalization (because using L2)

        distances, indices = self.index.search(query_vec, top_k)

        results = []

        for idx in indices[0]:
            if 0 <= idx < len(self.chunked_sections):
                results.append(self.chunked_sections[idx])

        return results