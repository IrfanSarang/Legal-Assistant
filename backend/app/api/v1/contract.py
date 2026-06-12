from fastapi import APIRouter, HTTPException
from app.schemas.contract import QueryRequest, QueryResponse
from app.rag.retriever import retrieve
from app.llm.contract_call import generate_response

router = APIRouter()

retriever = retrieve(namespace= "contract")

@router.post('/analyse', response_model=QueryResponse)
async def generate_answer(payload: QueryRequest):
    try:
        
        message = generate_response(payload.query, retriever)
        
        return QueryResponse(answer=message)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
        



