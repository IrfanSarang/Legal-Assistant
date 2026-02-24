from fastapi import APIRouter, HTTPException
from app.schemas.contract import ContractAnalysisRequest, ContractAnalysisResponse
from app.contractRag.retriever import Retriever
from app.llm.contract_call import DeepSeekLLM

router = APIRouter()

# Initialize once (do NOT load index here)
retriever = Retriever()
llm = DeepSeekLLM()


def build_prompt(law_context: str, contract_text: str) -> str:
    """
    Build strict RAG-safe prompt for local LLM.
    Prevents reasoning leakage and extra explanations.
    """
    return f"""
You are a legal assistant. Use the following retrieved context from Indian law to answer the question.
Do not make up answers; only answer based on the context.

Law Context:
{law_context}

Contract:
{contract_text}
"""


@router.post("/analyze", response_model=ContractAnalysisResponse)
def analyze_contract(request: ContractAnalysisRequest):
    try:
        # 🔹 Load FAISS index safely
        retriever.load()

        # 🔹 Retrieve relevant law sections
        law_chunks = retriever.retrieve(
            request.contract_text,
            top_k=request.top_k
        )

        if not law_chunks:
            raise HTTPException(
                status_code=404,
                detail="No relevant legal sections found."
            )

        # 🔹 Build context from retrieved chunks
        law_context = "\n\n".join(
            f"Section {chunk.get('section_number', 'N/A')}:\n{chunk.get('chunk_text', '')}"
            for chunk in law_chunks
        )

        # 🔹 Build strict prompt
        prompt = build_prompt(law_context, request.contract_text)

        # 🔹 Call LLM
        analysis = llm.generate(prompt)

        # 🔹 Return structured response
        return ContractAnalysisResponse(
            analysis=analysis,
            relevant_law_sections=law_chunks
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=400,
            detail="FAISS index not found. Please run law ingestion first."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )