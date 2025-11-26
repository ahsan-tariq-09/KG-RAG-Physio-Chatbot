from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    query: str


class EvidenceNode(BaseModel):
    id: str
    label: str
    type: Optional[str] = None


class EvidenceEdge(BaseModel):
    source: str
    target: str
    relation: str


class QueryResponse(BaseModel):
    answer: str
    nodes: List[EvidenceNode]
    edges: List[EvidenceEdge]
    raw_context: List[str]