import os
import pickle
import faiss
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer


class ContractFAISSManager:
    """
    Manages the FAISS index and the corresponding chunk list.

    Usage:
        model   = SentenceTransformer("nlpaueb/legal-bert-base-uncased"
        manager = ContractFAISSManager(model, "./data/vector_store")

        # Build once:
        manager.create_index(chunks)

        # On subsequent runs (index already on disk):
        manager.load_index()

    Attributes:
        index  : faiss.Index or None
        chunks : List[Dict]   — mirrors the FAISS vectors 1-to-1
    """

    def __init__(
        self,
        model:             SentenceTransformer,
        vector_store_path: str = "./data/vector_store",
    ):
        self.model       = model
        self.vector_dir  = vector_store_path
        self.index_file  = os.path.join(vector_store_path, "faiss_index.bin")
        self.chunks_file = os.path.join(vector_store_path, "chunks.pkl")
        self.index       = None
        self.chunks: List[Dict] = []

    # ------------------------------------------------------------------
    def create_index(self, chunked_sections: List[Dict]) -> None:
        """
        Embed all chunks, build a FAISS IndexFlatIP, and persist to disk.

        Args:
            chunked_sections : output of structure_sections_for_rag()
        """
        os.makedirs(self.vector_dir, exist_ok=True)

        print("[faiss] Generating embeddings...")
        texts      = [c["embedding_text"] for c in chunked_sections]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        embeddings = np.array(embeddings).astype("float32")

        # Normalise to unit vectors so inner-product == cosine similarity
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]
        index     = faiss.IndexFlatIP(dimension)
        index.add(embeddings)

        # Persist
        faiss.write_index(index, self.index_file)
        with open(self.chunks_file, "wb") as f:
            pickle.dump(chunked_sections, f)

        self.index  = index
        self.chunks = chunked_sections
        print(f"[faiss] ✅ Index saved — {index.ntotal} vectors, dim={dimension}")

    # ------------------------------------------------------------------
    def load_index(self) -> None:
        """
        Load a previously built FAISS index and chunk list from disk.

        Raises:
            FileNotFoundError if the index has not been built yet.
        """
        if not os.path.exists(self.index_file):
            raise FileNotFoundError(
                "FAISS index not found. Run create_index() first."
            )

        self.index = faiss.read_index(self.index_file)
        with open(self.chunks_file, "rb") as f:
            self.chunks = pickle.load(f)

        print(f"[faiss] ✅ Index loaded — {self.index.ntotal} vectors.")

    # ------------------------------------------------------------------
    def index_exists(self) -> bool:
        """Return True if a persisted index is available on disk."""
        return os.path.exists(self.index_file) and os.path.exists(self.chunks_file)