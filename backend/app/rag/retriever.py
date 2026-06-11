from app.rag.embedder import load_vectorstore

def retrieve(category=None, filename=None):
    """
    Retrieves a retriever object from the Pinecone vectorstore
    with optional filtering.
    """
    vectorstore = load_vectorstore()

    # Define search arguments based on provided filters
    search_kwargs = {"k": 5}
    
    if category:
        print(f"Applying filter: {{'category': '{category}'}}")
        search_kwargs["filter"] = {"category": category}
    elif filename:
        search_kwargs["filter"] = {"filename": filename}

    return vectorstore.as_retriever(search_kwargs=search_kwargs)