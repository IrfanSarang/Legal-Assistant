from app.rag.embedder import load_vectorstore

def retrieve(namespace=None, filename=None):
    """
    Retrieves a retriever object from the Pinecone vectorstore
    using specific namespace isolation.
    """
    # Load the vectorstore with the specific namespace
    vectorstore = load_vectorstore(namespace=namespace)

    search_kwargs = {"k": 5}
    
    # Optional: Keep filename filtering if you need sub-document precision
    if filename:
        search_kwargs["filter"] = {"filename": filename}

    return vectorstore.as_retriever(search_kwargs=search_kwargs)