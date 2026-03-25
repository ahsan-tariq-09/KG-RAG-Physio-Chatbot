from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class QueryRequest(BaseModel):
    query: str = Field(min_length=1)
    mode: Literal["vector", "hybrid"] = "vector"


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