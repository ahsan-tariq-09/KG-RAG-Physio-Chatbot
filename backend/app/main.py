from fastapi import FastAPI, Depends
from .config import get_settings, Settings
from .schemas import QueryRequest, QueryResponse
from .services.graphrag_service import GraphRAGService

app = FastAPI(title="KG-RAG Physio Chatbot")

# Single global service instance
_graphrag_service: GraphRAGService | None = None


def get_graphrag_service(settings: Settings = Depends(get_settings)) -> GraphRAGService:
    global _graphrag_service
    if _graphrag_service is None:
        _graphrag_service = GraphRAGService(
            neo4j_uri=settings.neo4j_uri,
            neo4j_user=settings.neo4j_user,
            neo4j_password=settings.neo4j_password,
            openai_api_key=settings.openai_api_key,
            index_name=settings.index_name,
        )
    return _graphrag_service


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(
    payload: QueryRequest,
    service: GraphRAGService = Depends(get_graphrag_service),
):
    return await service.query(payload.query)