from app.rag.embedder import load_vectorstore

def retrieve(category=None, filename = None):
    vectorstore = load_vectorstore()

    if category is None and filename is None:
        return vectorstore.as_retriever(search_kwargs={"k": 5})

    if category:
        return vectorstore.as_retriever(
            search_kwargs={"k": 5, "filter": {"category": category}}
        )

    if filename:
        return vectorstore.as_retriever(
            search_kwargs={"k": 5, "filter": {"filename": filename}}
        )
    

