from fastapi import APIRouter, HTTPException
from app.schemas.rag import QueryRequest, QueryResponse
from app.rag.retriever import retrieve
from app.llm.criminal_api import generate_response

router = APIRouter()

retriever = retrieve(category="criminal")

@router.post('/query', response_model=QueryResponse)
async def generate_answer(payload: QueryRequest):
    try:
        
        message = generate_response(payload.query, retriever)
        return QueryResponse(answer=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



