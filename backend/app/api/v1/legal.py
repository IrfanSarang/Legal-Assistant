from fastapi import APIRouter
from pydantic import BaseModel
from app.rag.retriever import RAGRetriever
from app.llm.deepseek import send_to_deepseek

router = APIRouter()
retriever = RAGRetriever()  # Load FAISS + chunks once at startup


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


def build_prompt(chunks: list, question: str) -> str:
    sections_seen = {}
    for c in chunks:
        sec = c["section_number"]
        if sec not in sections_seen:
            sections_seen[sec] = {
                "section_number": sec,
                "title": c.get("title", ""),
                "chunks": []
            }
        sections_seen[sec]["chunks"].append(c["chunk_text"])

    context_parts = []
    for sec_num, sec_data in sections_seen.items():
        title_line = f"Section {sec_num}"
        if sec_data["title"]:
            title_line += f" — {sec_data['title']}"
        combined_text = "\n".join(sec_data["chunks"])
        context_parts.append(f"{title_line}:\n{combined_text}")

    context = "\n\n---\n\n".join(context_parts)

    return f"""You are a senior Indian criminal lawyer specializing in Bharatiya Nyaya Sanhita (BNS) 2023.

Analyze the case and identify offences based ONLY on the retrieved legal sections below.

STRICT RULES — FOLLOW EXACTLY:
1. First identify WHO is the victim and WHO is the offender
2. Only apply offences to the OFFENDER, never to the victim
3. Right of private defence (Sections 37-41) applies ONLY when a person is defending themselves from an attack — it NEVER applies to the person who initiates an attack, commits rape, robbery, or any other offence
4. A rapist, robber, or attacker can NEVER claim self defence — do not suggest this under any circumstances
5. If rape sections (63/64/65) are retrieved, the accused committed rape — state the punishment clearly
6. List ALL offences committed with exact section numbers and punishments
7. Do NOT apply sections that are not in the retrieved context
8. If a person broke into a house AND stole — two offences
9. If a person kidnapped AND demanded ransom — two offences
10. If the VICTIM defends themselves from an attack — they are exercising their RIGHT OF PRIVATE DEFENCE (Sections 37-40) and are NOT guilty of any offence — state this clearly and do NOT charge the victim
11. Section 38 allows a victim to cause death or grievous harm if they reasonably apprehend death or grievous hurt from the attack — knives/weapons qualify as grievous hurt apprehension
12. Section 39 allows causing harm SHORT OF DEATH in self defence — if the victim only injured the attacker, this is fully within legal limits
13. Always conclude clearly: state who is guilty, who is protected by self defence, and what the punishment is for the offender

Retrieved Legal Sections:
{context}

Case:
{question}

Legal Analysis:"""

@router.post("/query")
def query_rag(req: QueryRequest):
    try:
        # 1️⃣ Smart retrieve — auto detects keyword vs story query
        top_chunks = retriever.smart_query(req.query, top_k=req.top_k)

        if not top_chunks:
            return {
                "question": req.query,
                "answer": "No relevant legal sections found for this query.",
                "retrieved_sections": [],
                "retrieved_chunks": []
            }

        # 2️⃣ Build improved prompt
        prompt = build_prompt(top_chunks, req.query)

        # 3️⃣ Send to DeepSeek LLM
        answer = send_to_deepseek(prompt)

        # 4️⃣ Return structured response
        return {
            "question": req.query,
            "answer": answer,
            "retrieved_sections": list({c["section_number"] for c in top_chunks}),
            "retrieved_chunks": [
                {
                    "section_number": c["section_number"],
                    "title": c.get("title", ""),
                    "chunk_type": c.get("chunk_type", ""),
                    "score": c.get("score", 0.0),
                    "chunk_text": c["chunk_text"]
                }
                for c in top_chunks
            ]
        }

    except Exception as e:
        return {"error": str(e)}
