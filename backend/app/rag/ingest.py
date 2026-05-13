from app.rag.extractor import load_all
from app.rag.splitter import splitter
from app.rag.embedder import create_vector
from dotenv import load_dotenv

load_dotenv()

print("\n")
print("============================")
print("Ingestion Process started....")


print("============================")
print("Loading the documennts")

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

