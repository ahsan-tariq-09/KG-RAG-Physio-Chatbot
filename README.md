# **KG-RAG Physical Rehabilitation Chatbot**

*A Knowledge-Graph-Enhanced Retrieval Augmented Generation System for Physical Therapy Queries*

This project implements the backend foundation of a rehabilitation-focused chatbot based on **Knowledge-Graph Retrieval-Augmented Generation (KG-RAG)**.
It integrates:

* **Neo4j** for the rehabilitation knowledge graph (built by collaborator)
* **Neo4j GraphRAG** for graph-aware retrieval following Microsoft’s GraphRAG principles
* **FastAPI** as the backend API layer
* **Gemini 3 Flash model** for generating answers grounded in retrieved graph evidence

The backend will later connect to a Streamlit frontend that visualizes subgraph evidence, enabling users to see how the system derived each answer.

The current stage focuses on backend architecture, Neo4j integration, GraphRAG scaffolding, and a working `/query` endpoint that returns:

* an LLM-generated answer
* an evidence subgraph (nodes + edges)
* retrieved text context

This is consistent with the system architecture described in the project proposal.

---

## **Project Goal**

The primary goal is to develop a chatbot that provides **accurate and explainable answers** to questions about physical rehabilitation exercises.
Instead of relying on plain text retrieval, the system grounds responses in **structured knowledge graph evidence**, reducing hallucinations and improving reasoning transparency.

This backend will serve as the foundation for later multimodal extensions such as CLIP embeddings, BLIP-2 captioning, FAISS similarity search, and Streamlit interface visualization.

---

## **Repository Structure**

```
kg-rag-physio/
  backend/
    app/
      main.py                # FastAPI entrypoint
      config.py              # Environment & settings
      schemas.py             # API models
      services/
        neo4j_client.py      # Neo4j connection + queries
        graphrag_service.py  # GraphRAG + LLM pipeline
    requirements.txt
  frontend/
    app.py                   # Streamlit UI (future)
  README.md
```
