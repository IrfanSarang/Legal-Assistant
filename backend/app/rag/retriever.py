import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

class RAGRetriever:
    def __init__(self, index_file="data/faiss/faiss_index.bin", chunks_file="data/faiss/chunks.pkl"):
        # Load persisted FAISS index
        self.index = faiss.read_index(index_file)

        # Load chunk metadata
        with open(chunks_file, "rb") as f:
            self.chunked_sections = pickle.load(f)

        # Load embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def query(self, query_text: str, top_k: int = 3):
        # Convert query to embedding
        query_vec = self.model.encode([query_text]).astype('float32')

        # Search FAISS index
        distances, indices = self.index.search(query_vec, top_k)

        # Return top chunks
        return [self.chunked_sections[idx] for idx in indices[0]]
