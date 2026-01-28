from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Tuple

from google import genai

from neo4j_graphrag.embeddings.sentence_transformers import SentenceTransformerEmbeddings
from neo4j_graphrag.retrievers import VectorRetriever, HybridRetriever

from .neo4j_client import Neo4jClient


@dataclass
class RetrievedItem:
    text: str
    score: float | None = None
    metadata: dict[str, Any] | None = None


class GraphRAGService:
    """
    Retrieval:
      - VectorRetriever or HybridRetriever from neo4j-graphrag
      - SentenceTransformerEmbeddings (open-source, local)

    Generation:
      - Gemini Developer API (google-genai SDK)

    Output:
      - Answer + evidence context + a small subgraph (nodes/edges) for later UI visualization.
    """

    def __init__(
        self,
        neo4j_client: Neo4jClient,
        gemini_api_key: str,
        gemini_model: str,
        vector_index_name: str,
        fulltext_index_name: str,
        top_k: int = 5,
    ):
        if not gemini_api_key:
            raise ValueError("Missing GEMINI_API_KEY. Set it in backend/.env")

        self.neo4j = neo4j_client
        self.top_k = top_k
        self.gemini_model = gemini_model

        # Open-source embeddings (local)
        self.embedder = SentenceTransformerEmbeddings(model="all-MiniLM-L6-v2")

        # Retrievers
        self.vector_retriever = VectorRetriever(
            driver=self.neo4j.driver,
            index_name=vector_index_name,
            embedder=self.embedder,
        )

        self.hybrid_retriever = HybridRetriever(
            driver=self.neo4j.driver,
            vector_index_name=vector_index_name,
            fulltext_index_name=fulltext_index_name,
            embedder=self.embedder,
        )

        # Gemini client
        # Quickstart shows API key can be provided; environment variable GEMINI_API_KEY also works. :contentReference[oaicite:8]{index=8}
        self.gemini = genai.Client(api_key=gemini_api_key)

    def _format_retrieval(self, raw: Any) -> List[RetrievedItem]:
        """
        neo4j-graphrag retrievers return (records, metadata).
        We convert to simple RetrievedItem objects.

        You may need to tweak this depending on your Neo4j schema and which properties you store.
        """
        records, meta = raw  # RawSearchResult according to docs
        items: List[RetrievedItem] = []

        for rec in records:
            # rec is a neo4j.Record; safest is to inspect typical keys
            # Common patterns: node properties contain 'text' or 'content' or 'chunk'
            data = rec.data()

            text = None
            # Try likely fields
            for key in ("text", "content", "chunk", "caption", "description"):
                if key in data and isinstance(data[key], str):
                    text = data[key]
                    break

            # If the record returns a node object
            if text is None:
                for v in data.values():
                    if hasattr(v, "get"):  # node-like
                        for key in ("text", "content", "chunk", "caption", "description", "name"):
                            try:
                                val = v.get(key)
                                if isinstance(val, str) and val.strip():
                                    text = val
                                    break
                            except Exception:
                                pass
                    if text:
                        break

            if not text:
                # Last resort
                text = str(data)

            items.append(RetrievedItem(text=text, score=data.get("score"), metadata=data))

        return items

    def retrieve(self, query: str, mode: str = "vector") -> List[RetrievedItem]:
        if mode == "hybrid":
            raw = self.hybrid_retriever.search(query_text=query, top_k=self.top_k)
        else:
            raw = self.vector_retriever.search(query_text=query, top_k=self.top_k)
        return self._format_retrieval(raw)

    def extract_evidence_subgraph(self, query: str) -> Tuple[list[dict], list[dict]]:
        """
        TEMPORARY evidence graph extraction.
        Your collaborator’s KG schema will determine the correct Cypher.
        This just finds nearby nodes/edges around name matches.
        """
        cypher = """
        MATCH (n)-[r]-(m)
        WHERE toLower(coalesce(n.name, '')) CONTAINS toLower($q)
           OR toLower(coalesce(m.name, '')) CONTAINS toLower($q)
        RETURN n, r, m
        LIMIT 50
        """
        with self.neo4j.driver.session() as session:
            rows = list(session.run(cypher, {"q": query}))

        nodes: dict[str, dict] = {}
        edges: list[dict] = []

        for row in rows:
            n = row["n"]
            m = row["m"]
            r = row["r"]

            for node in (n, m):
                node_id = node.element_id
                if node_id not in nodes:
                    nodes[node_id] = {
                        "id": node_id,
                        "label": node.get("name", node_id),
                        "type": next(iter(node.labels), None),
                    }

            edges.append(
                {
                    "source": n.element_id,
                    "target": m.element_id,
                    "relation": r.type,
                }
            )

        return list(nodes.values()), edges

    def generate_answer(self, query: str, context_items: List[RetrievedItem]) -> str:
        context_block = "\n\n".join(
            [f"[Evidence {i+1}] {item.text}" for i, item in enumerate(context_items)]
        )

        prompt = f"""
You are a physical rehabilitation assistant. Answer the user's question using ONLY the evidence.
If the evidence is insufficient, say what is missing and ask a single follow-up question.

User question:
{query}

Evidence:
{context_block}

Write a clear, safe, non-medical, educational answer.
Include:
- exercise name(s)
- muscles/joints involved (if present in evidence)
- 1-2 safety notes (generic, non-clinical)
"""

        # Gemini API quickstart uses generateContent. :contentReference[oaicite:9]{index=9}
        resp = self.gemini.models.generate_content(
            model=self.gemini_model,
            contents=prompt,
        )
        # SDK typically returns resp.text
        return getattr(resp, "text", str(resp))

    def query(self, query: str, mode: str = "vector") -> tuple[str, list[str], list[dict], list[dict]]:
        retrieved = self.retrieve(query, mode=mode)
        answer = self.generate_answer(query, retrieved)
        nodes, edges = self.extract_evidence_subgraph(query)
        raw_context = [x.text for x in retrieved]
        return answer, raw_context, nodes, edges