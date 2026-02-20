from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class ChunkResponse(BaseModel):
    section_number: str
    title: str
    chunk_index: int
    chunk_text: str
    illustrations: list
    explanations: list
    provisos: list

class QueryResponse(BaseModel):
    results: list[ChunkResponse]
