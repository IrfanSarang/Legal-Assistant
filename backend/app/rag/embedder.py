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


def create_vector(chunks):
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
       print(f"Created Pinecone index: {PINECONE_INDEX_NAME}")

   vectorstore = PineconeVectorStore.from_documents(
       documents=chunks,
       embedding=embedder,
       index_name=PINECONE_INDEX_NAME,
       pinecone_api_key=PINECONE_API_KEY
   )
   print("Vectors uploaded to Pinecone successfully.")
   return vectorstore


def load_vectorstore():
   embedder = get_embedder()
   vectorstore = PineconeVectorStore(
       index_name=PINECONE_INDEX_NAME,
       embedding=embedder,
       pinecone_api_key=PINECONE_API_KEY
   )
   return vectorstore