from fastapi import  HTTPException
from app.schemas.contract import ContractAnalysisRequest, ContractAnalysisResponse
from app.contractRag.retriever import Retriever
from app.llm.contract_call import DeepSeekLLM
from fastapi import APIRouter

router = APIRouter()

  # Initialize objects (NO loading here)
retriever = Retriever()
llm = DeepSeekLLM()


@router.post("/analyze", response_model=ContractAnalysisResponse)
def analyze_contract(request: ContractAnalysisRequest):
      # 🔹 Load index safely
    try:
        retriever.load()
    except FileNotFoundError:
        raise HTTPException(
            status_code=400,
            detail="FAISS index not found. Please run law ingestion first."
        )
      # 1️⃣ Retrieve relevant law sections
    law_chunks = retriever.retrieve(
        request.contract_text,
        top_k=request.top_k
    )

    if not law_chunks:
        raise HTTPException(
            status_code=404,
            detail="No relevant legal sections found."
        )
    law_context = "\n\n".join(
    chunk["chunk_text"] for chunk in law_chunks
     )
      # 2️⃣ Build prompt
    prompt = f"""
You are a legal expert.

IMPORTANT:
- Do NOT start with phrases like "Okay", "I need to", "The task is", or any reasoning text.
- Do NOT explain your thinking process.
- Start directly with the clause analysis.
- Do NOT mention the instructions.

For each problematic clause:

1. Explain the clause in simple words.
2. State clearly whether it violates any section (mention section number).
3. Explain the legal consequence in simple terms.
4. Give one short real-life example of what could happen.

Keep the explanation short and simple.
Maximum 300 words.

Law Context:
{law_context}

Contract:
{request.contract_text}
"""

      # 3️⃣ Call LLM
    analysis = llm.generate(prompt)

    return {
        "analysis": analysis,
        "relevant_law_sections": law_chunks
    }