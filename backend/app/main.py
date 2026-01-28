from fastapi import FastAPI, Depends
from .config import Settings, get_settings
from .schemas import QueryRequest, QueryResponse, EvidenceNode, EvidenceEdge
from .services.neo4j_client import Neo4jClient
from .services.graphrag_service import GraphRAGService

app = FastAPI(title="KG-RAG Physio (Gemini)")

_service: GraphRAGService | None = None
_neo4j: Neo4jClient | None = None


def get_service(settings: Settings = Depends(get_settings)) -> GraphRAGService:
    global _service, _neo4j

    if _service is None:
        _neo4j = Neo4jClient(
            uri=settings.neo4j_uri,
            user=settings.neo4j_user,
            password=settings.neo4j_password,
            database=settings.neo4j_database,
        )

        _service = GraphRAGService(
            neo4j_client=_neo4j,
            gemini_api_key=settings.gemini_api_key,
            gemini_model=settings.gemini_model,
            vector_index_name=settings.vector_index_name,
            fulltext_index_name=settings.fulltext_index_name,
            top_k=settings.top_k,
        )

    return _service


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query_endpoint(payload: QueryRequest, service: GraphRAGService = Depends(get_service)):
    answer, raw_context, nodes_raw, edges_raw = service.query(payload.query, mode=payload.mode)

    nodes = [EvidenceNode(**n) for n in nodes_raw]
    edges = [EvidenceEdge(**e) for e in edges_raw]

    return QueryResponse(
        answer=answer,
        nodes=nodes,
        edges=edges,
        raw_context=raw_context,
    )