from fastapi import APIRouter, HTTPException
from app.schemas.contract import ContractAnalysisRequest, ContractAnalysisResponse
from app.contractRag.retriever import Retriever
from app.llm.contract_call import DeepSeekLLM
import re 
router = APIRouter()

# Initialize once (do NOT load index here)
retriever = Retriever()
llm = DeepSeekLLM()

def expand_query(contract_text: str) -> str:
    return (
        "Indian Contract Act validity enforceability "
        "consideration void voidable agreement competent parties "
        "free consent coercion undue influence fraud misrepresentation "
        "threat force sound mind capacity lawful object | "
        + contract_text
    )


def build_prompt(law_context: str, contract_text: str) -> str:
    return f"""You are a legal assistant specializing in Indian Contract Law.

CRITICAL LEGAL RULES YOU MUST FOLLOW:
- A person of UNSOUND MIND cannot enter any contract — agreement is VOID AB INITIO (Section 11, 12)
- A MINOR cannot enter any contract — agreement is VOID AB INITIO (Section 11)
- Consent obtained by COERCION, FRAUD, MISREPRESENTATION or UNDUE INFLUENCE — agreement is VOIDABLE at the option of the affected party (Section 14, 15, 16, 17, 18, 19)
- COERCION means threatening to commit any act forbidden by law (Section 15)
- VOID means the agreement never existed in law
- VOIDABLE means valid until the affected party chooses to cancel it
- Do NOT confuse void with voidable
"- Consent obtained by COERCION is NOT free consent — agreement is VOIDABLE at victim's option (Section 14, 15, 19)\n"
"- COERCION = threatening any act forbidden by IPC — consent under threat is NEVER free\n"

Retrieved Law Sections:
{law_context}

Contract / Legal Question:
{contract_text}

Instructions:
- Identify which section MOST DIRECTLY applies first
- State clearly if the agreement is VOID or VOIDABLE and why
- Give final conclusion

Analysis:"""


@router.post("/analyze", response_model=ContractAnalysisResponse)
def analyze_contract(request: ContractAnalysisRequest):
    try:
        # 🔹 Load FAISS index safely
        retriever.load()

        # 🔹 Retrieve relevant law sections
        law_chunks = retriever.retrieve(
        expand_query(request.contract_text),
        top_k=request.top_k
        )

        if not law_chunks:
            raise HTTPException(
                status_code=404,
                detail="No relevant legal sections found."
            )

        # 🔹 Build context from retrieved chunks
        law_context = "\n\n".join(
            f"Section {chunk.get('metadata', {}).get('section', 'N/A')} — "
            f"{chunk.get('metadata', {}).get('title', '')}:\n"
            f"{chunk.get('content', '')}"
            for chunk in law_chunks
        )

        # 🔹 Build strict prompt
        prompt = build_prompt(law_context, request.contract_text)

        # 🔹 Call LLM
        analysis = llm.generate(prompt)

        # 🔹 Return structured response
        relevant_sections = [
        {
            "section": chunk.get("metadata", {}).get("section", "N/A"),
            "title":   chunk.get("metadata", {}).get("title", ""),
            "chapter": chunk.get("metadata", {}).get("chapter_title", ""),
            "content": re.sub(r'^\[Legal concepts:[^\]]+\]\n?', '', 
                            chunk.get("content", "")),  # ← strip tag
        }
        for chunk in law_chunks
    ]

        return ContractAnalysisResponse(
            analysis=analysis,
            relevant_law_sections=relevant_sections
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