from fastapi import APIRouter
from pydantic import BaseModel
from app.rag.retriever import RAGRetriever
from app.llm.deepseek import send_to_deepseek

router = APIRouter()
retriever = RAGRetriever()  # Load FAISS + chunks once

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

def build_prompt(chunks, question: str) -> str:
    """
    Convert retrieved chunks into a single prompt for LLM.
    """
    context = "\n\n".join([f"Section {c['section_number']}:\n{c['chunk_text']}" for c in chunks])
    return f"""
You are a legal assistant. Use the following retrieved context from Indian law to answer the question.
Do not make up answers; only answer based on the context.

Context:
{context}

Question: {question}

Answer:
"""

@router.post("/query")
def query_rag(req: QueryRequest):
    try:
            
        # 1️⃣ Retrieve top-k chunks
        top_chunks = retriever.query(req.query, req.top_k)

        # 2️⃣ Build prompt
        prompt = build_prompt(top_chunks, req.query)

        # 3️⃣ Send to DeepSeek LLM
        answer = send_to_deepseek(prompt)

        # 4️⃣ Return structured response
        return {
            "question": req.query,
            "answer": answer,
            "retrieved_chunks": top_chunks
        }

    except Exception as e:
        return {"error": str(e)}
