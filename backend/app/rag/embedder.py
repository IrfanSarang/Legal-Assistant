from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

VECTORSTORE_PATH = "vectorstore"

def get_embedder():
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",  # fast + accurate
        model_kwargs={"device": "cpu"},        # change to "gpu" if you have GPU
        encode_kwargs={"normalize_embeddings": True}
    )
    return embedding_model

def create_vector(chunks):
    embedder = get_embedder()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedder,
        persist_directory=VECTORSTORE_PATH
    )
    print("Vectorstore created and saved.")
    return vectorstore

def load_vectorstore():
    embedder = get_embedder()
    vectorstore = Chroma(
        persist_directory=VECTORSTORE_PATH,
        embedding_function=embedder
    )
    return vectorstore