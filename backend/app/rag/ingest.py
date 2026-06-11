from dotenv import load_dotenv
from app.rag.extractor import load_all
from app.rag.splitter import splitter
from app.rag.embedder import create_vector

load_dotenv()

if __name__ == "__main__":
    print("\n============================")
    print("Ingestion Process started....")

    print("============================")
    print("Loading the documents")
    docs = load_all("data")
    print(docs[0].page_content[:100])

    print("============================")
    print("Producing Chunks...")
    chunks = splitter(docs)

    print("============================")
    print("Generating Embeddings and Storing...")
    create_vector(chunks)

    print("============================")
    print("Successfully Completed Ingestion Process!!")