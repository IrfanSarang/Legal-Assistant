import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

PINECONE_API_KEY   = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "legal-assistant")


def get_embedder():
   embedding_model = HuggingFaceEmbeddings(
       model_name="sentence-transformers/all-MiniLM-L6-v2",  # 80MB, 384-dim
       model_kwargs={"device": "cpu"},
       encode_kwargs={"normalize_embeddings": True}
   )
   return embedding_model


def create_vector(chunks, namespace=None):
    embedder = get_embedder()
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Create index if it doesn't exist
    existing = [i.name for i in pc.list_indexes()]
    if PINECONE_INDEX_NAME not in existing:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embedder,
        index_name=PINECONE_INDEX_NAME,
        pinecone_api_key=PINECONE_API_KEY,
        namespace=namespace  # Added namespace
    )
    print(f"Vectors uploaded to namespace '{namespace}' successfully.")
    return vectorstore


def load_vectorstore(namespace=None):
    embedder = get_embedder()
    vectorstore = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embedder,
        pinecone_api_key=PINECONE_API_KEY,
        namespace=namespace  # Added namespace
    )
    return vectorstore