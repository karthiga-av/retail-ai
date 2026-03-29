from fastapi import APIRouter
from app.schemas.request import QueryRequest
from app.schemas.response import QueryResponse
from app.services.query_service import process_query

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    result = process_query(request.query)
    return QueryResponse(response=result)