# app/rag/faiss_manager.py
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
import os

class FAISSManager:
    """
    Fixed FAISSManager:
    - Cosine similarity (IndexFlatIP + L2 normalize)
    - multi-qa-MiniLM-L6-cos-v1 model
    """

    def __init__(
        self,
        embedding_model_name="multi-qa-MiniLM-L6-cos-v1",
        index_file="data/faiss/faiss_index.bin",
        chunks_file="data/faiss/chunks.pkl"
    ):
        self.model = SentenceTransformer(embedding_model_name)
        self.index_file = index_file
        self.chunks_file = chunks_file
        self.index = None
        self.chunked_sections = []

    def create_index(self, chunked_sections: list):
        print("Generating embeddings...")
        texts = [c["chunk_text"] for c in chunked_sections]
        embeddings = self.model.encode(texts, show_progress_bar=True, batch_size=64)
        embeddings = np.array(embeddings).astype("float32")
        faiss.normalize_L2(embeddings)
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(embeddings)
        os.makedirs(os.path.dirname(self.index_file), exist_ok=True)
        faiss.write_index(index, self.index_file)
        with open(self.chunks_file, "wb") as f:
            pickle.dump(chunked_sections, f)
        print(f"✅ Index saved: {index.ntotal} vectors")
        self.index = index
        self.chunked_sections = chunked_sections

    def load_index(self):
        self.index = faiss.read_index(self.index_file)
        with open(self.chunks_file, "rb") as f:
            self.chunked_sections = pickle.load(f)
        print(f"✅ Loaded {self.index.ntotal} vectors")

    def query(self, query_text: str, top_k: int = 5) -> list:
        if self.index is None:
            raise ValueError("Index not loaded.")
        query_vec = self.model.encode([query_text]).astype("float32")
        faiss.normalize_L2(query_vec)
        distances, indices = self.index.search(query_vec, top_k)
        results = []
        for score, idx in zip(distances[0], indices[0]):
            chunk = self.chunked_sections[idx].copy()
            chunk["score"] = round(float(score), 4)
            results.append(chunk)
        return results