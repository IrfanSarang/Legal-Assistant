from langchain_text_splitters import RecursiveCharacterTextSplitter


#Splitting function
def splitter(all_docs):

    splits = RecursiveCharacterTextSplitter(
        chunk_size = 400,
        chunk_overlap = 150,
        separators=["\nSection ", "\n\n", "\n", " "]
    )

    chunks = splits.split_documents(all_docs)
    print(f"Total chunks: {len(chunks)}")
    return chunks